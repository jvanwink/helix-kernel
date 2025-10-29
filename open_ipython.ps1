# open_ipython.ps1

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
wt -w 0 sp -v -d . --profile "cmder" cmd.exe /k "%CMDER_ROOT%\vendor\init.bat & conda activate $condaEnv & ipython"
