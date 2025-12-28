# Generate all individual weapon and armor files for Vanilla Expanded mods
$processed = Get-Content "F:\Python Apps\EPIC\vanilla_expanded_processed.json" | ConvertFrom-Json

$basePath = "F:\Python Apps\EPIC\RULES\Combat"

# Mod to folder mapping
$modFolders = @{
    "Vanilla Weapons Expanded" = "Vanilla-Weapons-Expanded"
    "Vanilla Weapons Expanded - Laser" = "Vanilla-Weapons-Expanded\Laser"
    "Vanilla Weapons Expanded - Grenades" = "Vanilla-Weapons-Expanded\Grenades"
    "Vanilla Weapons Expanded - Heavy Weapons" = "Vanilla-Weapons-Expanded\Heavy-Weapons"
    "Vanilla Weapons Expanded - Coilguns" = "Vanilla-Weapons-Expanded\Coilguns"
    "Vanilla Weapons Expanded - Makeshift" = "Vanilla-Weapons-Expanded\Makeshift"
    "Vanilla Weapons Expanded - Frontier" = "Vanilla-Weapons-Expanded\Frontier"
    "Vanilla Weapons Expanded - Non-Lethal" = "Vanilla-Weapons-Expanded\Non-Lethal"
    "Vanilla Weapons Expanded - Tribal" = "Vanilla-Weapons-Expanded\Tribal"
    "Vanilla Persona Weapons Expanded" = "Vanilla-Weapons-Expanded\Persona-Weapons"
    "Vanilla Factions Expanded - Settlers" = "Vanilla-Factions-Expanded\Settlers"
    "Vanilla Factions Expanded - Ancients" = "Vanilla-Factions-Expanded\Ancients"
    "Vanilla Factions Expanded - Pirates" = "Vanilla-Factions-Expanded\Pirates"
    "Vanilla Factions Expanded - Classical" = "Vanilla-Factions-Expanded\Classical"
    "Vanilla Armour Expanded" = "Vanilla-Armor-Expanded"
    "Vanilla Apparel Expanded" = "Vanilla-Armor-Expanded\Apparel"
    "Vanilla Apparel Expanded - Accessories" = "Vanilla-Armor-Expanded\Accessories"
}

function Sanitize-FileName {
    param($name)
    $name = $name -replace '[<>:"/\\|?*]', ''
    $name = $name -replace '\s+', '-'
    return $name
}

function Generate-WeaponFile {
    param($weapon, $folderPath)
    
    $fileName = Sanitize-FileName $weapon.label
    if (-not $fileName) { $fileName = Sanitize-FileName $weapon.defName }
    
    $filePath = Join-Path $folderPath "$fileName.md"
    
    $isVehicleScale = $weapon.defName -like "*Warcasket*"
    $vehicleNote = if ($isVehicleScale) { "`n**Note:** This is a huge, vehicle-scale weapon integrated into warcasket armor systems. Too large for normal pawns to use - only warcasket users can operate this massive weapon." } else { "" }
    
    $content = @"
# $($weapon.label)

**Source:** $($weapon.mod) (Mod)

**Note:** Statistics converted from Rimworld values to Advanced Fighting Fantasy damage track system.$vehicleNote

## Damage Track

| Roll | 1 | 2 | 3 | 4 | 5 | 6 | 7+ |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Damage | $($weapon.affDamageTrack[0]) | $($weapon.affDamageTrack[1]) | $($weapon.affDamageTrack[2]) | $($weapon.affDamageTrack[3]) | $($weapon.affDamageTrack[4]) | $($weapon.affDamageTrack[5]) | $($weapon.affDamageTrack[6]) |

## Statistics

- **Original Rimworld Damage:** ~$([math]::Round($weapon.damage, 1))
- **Original Rimworld DPS:** ~$([math]::Round($weapon.dps, 2))
$(if ($weapon.range -gt 0) { "- **Range:** $([math]::Round($weapon.range, 1))" })
- **Type:** $(if ($weapon.isMelee) { "Melee$(if ($isVehicleScale) { ' (integrated, vehicle-scale)' } else { '' })" } else { "Ranged$(if ($isVehicleScale) { ' (integrated, vehicle-scale)' } else { '' })" })
- **Tech Level:** $($weapon.techLevel)
- **Mod:** $($weapon.mod)
$(if ($isVehicleScale) { "- **Special:** Integrated into warcasket armor, vehicle-scale damage, huge weapon" })

## Description

$($weapon.description)

"@
    
    $content | Out-File $filePath -Encoding UTF8 -NoNewline
}

function Generate-ArmorFile {
    param($armor, $folderPath)
    
    $fileName = Sanitize-FileName $armor.label
    if (-not $fileName) { $fileName = Sanitize-FileName $armor.defName }
    
    $filePath = Join-Path $folderPath "$fileName.md"
    
    $maxArmor = [Math]::Max($armor.sharpArmor, [Math]::Max($armor.bluntArmor, $armor.heatArmor))
    $affTrack = @(0,0,0,0,0,0,1)
    if ($maxArmor -le 0.1) { $affTrack = @(0,0,0,0,0,0,1) }
    elseif ($maxArmor -le 0.2) { $affTrack = @(0,0,0,0,0,1,1) }
    elseif ($maxArmor -le 0.3) { $affTrack = @(0,0,0,0,1,1,2) }
    elseif ($maxArmor -le 0.4) { $affTrack = @(0,0,0,1,1,2,2) }
    elseif ($maxArmor -le 0.5) { $affTrack = @(0,0,1,1,2,2,3) }
    elseif ($maxArmor -le 0.6) { $affTrack = @(0,1,1,2,2,3,3) }
    elseif ($maxArmor -le 0.7) { $affTrack = @(0,1,1,2,2,3,4) }
    elseif ($maxArmor -le 0.8) { $affTrack = @(1,1,2,2,3,4,5) }
    else { $affTrack = @(1,2,2,3,3,4,5) }
    
    $content = @"
# $($armor.label)

**Source:** $($armor.mod) (Mod)

**Note:** Statistics converted from Rimworld protection values to Advanced Fighting Fantasy protection track system.

## Protection Track

| Roll | 1 | 2 | 3 | 4 | 5 | 6 | 7+ |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Protection | $($affTrack[0]) | $($affTrack[1]) | $($affTrack[2]) | $($affTrack[3]) | $($affTrack[4]) | $($affTrack[5]) | $($affTrack[6]) |

## Statistics

- **Original Rimworld Sharp Protection:** ~$([math]::Round($armor.sharpArmor * 100, 1))%
- **Original Rimworld Blunt Protection:** ~$([math]::Round($armor.bluntArmor * 100, 1))%
- **Original Rimworld Heat Protection:** ~$([math]::Round($armor.heatArmor * 100, 1))%
- **Body Parts:** $($armor.bodyPartGroups -join ', ')
- **Layers:** $($armor.layers -join ', ')
- **Tech Level:** $($armor.techLevel)
- **Mod:** $($armor.mod)

## Description

$($armor.description)

"@
    
    $content | Out-File $filePath -Encoding UTF8 -NoNewline
}

# Create weapon files
Write-Host "Creating weapon files..."
$weaponCount = 0
foreach ($weapon in $processed.weapons) {
    if (-not $modFolders.ContainsKey($weapon.mod)) {
        Write-Host "Unknown mod: $($weapon.mod) for $($weapon.defName)"
        continue
    }
    
    $folderName = $modFolders[$weapon.mod]
    $folderPath = Join-Path $basePath "Weapons\Rimworld\$folderName"
    
    if (-not (Test-Path $folderPath)) {
        New-Item -ItemType Directory -Path $folderPath -Force | Out-Null
    }
    
    Generate-WeaponFile $weapon $folderPath
    $weaponCount++
    
    if ($weaponCount % 20 -eq 0) {
        Write-Host "Created $weaponCount weapon files..."
    }
}
Write-Host "Created $weaponCount weapon files total."

# Create armor files
Write-Host "Creating armor files..."
$armorCount = 0
foreach ($armor in $processed.armors) {
    if (-not $modFolders.ContainsKey($armor.mod)) {
        Write-Host "Unknown mod: $($armor.mod) for $($armor.defName)"
        continue
    }
    
    $folderName = $modFolders[$armor.mod]
    $folderPath = Join-Path $basePath "Armor\Rimworld\$folderName"
    
    if (-not (Test-Path $folderPath)) {
        New-Item -ItemType Directory -Path $folderPath -Force | Out-Null
    }
    
    Generate-ArmorFile $armor $folderPath
    $armorCount++
    
    if ($armorCount % 20 -eq 0) {
        Write-Host "Created $armorCount armor files..."
    }
}
Write-Host "Created $armorCount armor files total."

Write-Host "`nAll files generated successfully!"



