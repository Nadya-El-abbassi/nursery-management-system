# copie feature_m3_ai vers app/ avant push GitHub
$base = Split-Path $PSScriptRoot -Parent

Copy-Item "$base\feature_m3_ai\services\dashboard_service.py" "$base\app\services\" -Force
Copy-Item "$base\feature_m3_ai\services\ai_service.py" "$base\app\services\" -Force
Copy-Item "$base\feature_m3_ai\routes\dashboard.py" "$base\app\routes\" -Force
Copy-Item "$base\feature_m3_ai\routes\ai.py" "$base\app\routes\" -Force
Copy-Item "$base\feature_m3_ai\templates\base.html" "$base\app\templates\" -Force
Copy-Item "$base\feature_m3_ai\templates\index.html" "$base\app\templates\" -Force
Copy-Item "$base\feature_m3_ai\templates\ai" "$base\app\templates\ai" -Recurse -Force
Copy-Item "$base\feature_m3_ai\static\*" "$base\app\static\" -Recurse -Force

Write-Host "M3 synchronise vers app/ - pret pour git add app/"
