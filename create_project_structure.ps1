# Defina o caminho base onde o projeto será criado
$basePath = "C:\Users\zaack\PycharmProjects\CapacitatedVehicleRoutingProblem-Dashboard"

# Lista de diretórios a serem criados
$folders = @(
    "$basePath",
    "$basePath\data",
    "$basePath\database",
    "$basePath\models",
    "$basePath\analysis"
)

# Criação dos diretórios
foreach ($folder in $folders) {
    if (-not (Test-Path -Path $folder)) {
        New-Item -Path $folder -ItemType Directory | Out-Null
        Write-Host "Diretório criado: $folder"
    } else {
        Write-Host "Diretório já existe: $folder"
    }
}

# Diretórios que precisam do __init__.py
$pythonPackages = @(
    "$basePath\database",
    "$basePath\models",
    "$basePath\analysis"
)

# Criar arquivos __init__.py
foreach ($package in $pythonPackages) {
    $initFile = Join-Path $package "__init__.py"
    if (-not (Test-Path -Path $initFile)) {
        New-Item -Path $initFile -ItemType File | Out-Null
        Write-Host "Arquivo __init__.py criado em: $package"
    } else {
        Write-Host "Arquivo __init__.py já existe em: $package"
    }
}
