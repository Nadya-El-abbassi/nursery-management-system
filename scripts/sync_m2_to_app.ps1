#copie feature_m2_crud vers app/ avant push GitHub
$base = Split-Path $PSScriptRoot -Parent

Copy-Item "$base\feature_m2_crud\repositories\*" "$base\app\repositories\" -Force
Copy-Item "$base\feature_m2_crud\services\plant_service.py" "$base\app\services\" -Force
Copy-Item "$base\feature_m2_crud\services\sale_service.py" "$base\app\services\" -Force
Copy-Item "$base\feature_m2_crud\services\stock_alert_service.py" "$base\app\services\" -Force
Copy-Item "$base\feature_m2_crud\routes\plants.py" "$base\app\routes\" -Force
Copy-Item "$base\feature_m2_crud\routes\sales.py" "$base\app\routes\" -Force
Copy-Item "$base\feature_m2_crud\routes\categories.py" "$base\app\routes\" -Force
Copy-Item "$base\feature_m2_crud\templates\plants" "$base\app\templates\plants" -Recurse -Force
Copy-Item "$base\feature_m2_crud\templates\sales" "$base\app\templates\sales" -Recurse -Force

Write-Host "M2 synchronise vers app/ - pret pour git add app/"
