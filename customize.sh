#!/bin/bash
# customize.sh - Script de customização executado dentro do chroot ARM64
# WhaleOS - Baseado em Ubuntu Touch Core

set -e

echo "[WhaleOS] Iniciando customização do rootfs..."

# 1. Alterar hostname do sistema
echo "CustomTouchOS" > /etc/hostname
sed -i 's/localhost/CustomTouchOS/g' /etc/hosts
echo "[WhaleOS] Hostname alterado para CustomTouchOS"

# 2. Definir caminhos dos ativos
ICON_DEST="/usr/share/icons/whaleos/apps/64"
BG_DEST="/usr/share/backgrounds/whaleos"
GENERATED_ICON_SRC="/usr/share/icons/whaleos/apps/64" # Já estão no local correto via generate_assets.py
GENERATED_BG_SRC="/usr/share/backgrounds/whaleos/whaleos-default.jpg"

# 3. Copiar wallpaper alternativo da raiz do repo (se existir no /tmp do chroot)
if [ -f "/tmp/wallpaper.jpg" ]; then
    cp /tmp/wallpaper.jpg "${BG_DEST}/whaleos-alternative.jpg"
    chmod 644 "${BG_DEST}/whaleos-alternative.jpg"
    echo "[WhaleOS] Wallpaper alternativo copiado do repositório."
fi

# 4. Garantir permissões corretas nos ativos procedurais
chmod -R 644 "${ICON_DEST}"/*.png 2>/dev/null || true
chmod 644 "${GENERATED_BG_SRC}" 2>/dev/null || true
chown -R root:root /usr/share/icons/whaleos /usr/share/backgrounds/whaleos

# 5. Configurar tema e wallpaper padrão para Lomiri/Ubuntu Touch
# Criar override de configuração dconf/gsettings para sessão padrão
mkdir -p /etc/dconf/db/local.d
cat > /etc/dconf/db/local.d/00-whaleos-defaults << 'EOF'
[com/canonical/unity-greeter]
background='/usr/share/backgrounds/whaleos/whaleos-default.jpg'

[org/gnome/desktop/background]
picture-uri='file:///usr/share/backgrounds/whaleos/whaleos-default.jpg'
picture-options='zoom'

[org/gnome/desktop/interface]
icon-theme='whaleos'
EOF

# Atualizar banco de dados dconf
if command -v dconf &> /dev/null; then
    dconf update
    echo "[WhaleOS] Banco de dados dconf atualizado."
else
    echo "[WhaleOS] Aviso: dconf não encontrado. Configurações salvas apenas em arquivo."
fi

# 6. Criar índice de tema de ícones básico
cat > /usr/share/icons/whaleos/index.theme << 'EOF'
[Icon Theme]
Name=WhaleOS
Comment=Procedurally generated flat icon theme for WhaleOS
Directories=apps/64
Type=Fixed
Size=64
MinSize=64
MaxSize=64

[apps/64]
Size=64
Type=Fixed
Context=Applications
EOF

# 7. Limpeza de cache e logs dentro do chroot
rm -rf /var/cache/apt/archives/*.deb
rm -rf /tmp/*
rm -rf /var/tmp/*

echo "[WhaleOS] Customização concluída com sucesso!"
