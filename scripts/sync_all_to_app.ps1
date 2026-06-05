# Synchronise M2 + M3 vers app/ (avant push ou test clone)
& "$PSScriptRoot\sync_m2_to_app.ps1"
& "$PSScriptRoot\sync_m3_to_app.ps1"
Write-Host "Synchronisation complete."
