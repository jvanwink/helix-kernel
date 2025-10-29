# start_python_kernel.ps1

# Read the conda environment from the project-specific configuration file
$projectConfigFile = "run_config.txt"

$condaEnv = $null

# Read the configuration file
if (Test-Path $projectConfigFile) {
    $configContent = Get-Content $projectConfigFile -Raw
    $configLines = $configContent -split "`n"
    foreach ($line in $configLines) {
        if ($line -match "^conda_env=(.*)$") {
            $condaEnv = $matches[1].Trim()
        }
    }

    # Check if both configurations were found
    if (-not $condaEnv) {
        Write-Error "Conda environment not specified in the configuration file"
        exit 1
    }
} else {
    Write-Error "Configuration file not found"
    exit 1
}

Start-Process cmd.exe -ArgumentList "/c conda activate $condaEnv && jupyter kernel --KernelManager.connection_file jup_kernel.json" -NoNewWindow -RedirectStandardOutput "NUL"

$currentPath = Get-Location
$connectionFilePath = Join-Path -Path $currentPath -ChildPath "jup_kernel.json"

Start-Sleep -Seconds 2

wt -w 0 sp -v -d . --profile "cmder" cmd.exe /k "%CMDER_ROOT%\vendor\init.bat & conda activate $condaEnv & jupyter console --existing $connectionFilePath --ZMQTerminalInteractiveShell.include_other_output True --ZMQTerminalInteractiveShell.other_output_prefix 'HX: ' --ZMQTerminalInteractiveShell.true_color True"
