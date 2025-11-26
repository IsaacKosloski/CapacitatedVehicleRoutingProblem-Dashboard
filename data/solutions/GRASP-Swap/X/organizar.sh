#!/bin/bash

# Diretório base onde estão os arquivos e pastas
DIR="/mnt/c/Users/zaack/PycharmProjects/CapacitatedVehicleRoutingProblem-Dashboard/data/solutions/GRASP-Swap/X"

# Verifica se o diretório existe
if [ ! -d "$DIR" ]; then
    echo "Erro: Diretório '$DIR' não encontrado"
    exit 1
fi

cd "$DIR" || exit 1

echo "Organizando arquivos nas pastas correspondentes..."

# Contador para estatísticas
count=0

# Para cada arquivo .sol que termina com -XX.sol
for arquivo in X-*-[0-9][0-9].sol; do
    # Verifica se o padrão encontrou algo
    [ -e "$arquivo" ] || continue

    # Verifica se é um arquivo regular
    if [ -f "$arquivo" ]; then
        # Remove a extensão .sol primeiro
        nome_sem_ext="${arquivo%.sol}"

        # Extrai o nome base removendo os últimos 3 caracteres (-XX)
        pasta="${nome_sem_ext%-[0-9][0-9]}"

        echo "Processando: $arquivo -> Pasta: $pasta"

        # Verifica se a pasta correspondente existe
        if [ -d "$pasta" ]; then
            # Move o arquivo para a pasta
            mv "$arquivo" "$pasta/"
            echo "✓ Movido: $arquivo -> $pasta/"
            ((count++))
        else
            echo "✗ Aviso: Pasta '$pasta' não encontrada para o arquivo '$arquivo'"
        fi
    fi
done

echo ""
echo "Concluído! $count arquivos foram organizados."