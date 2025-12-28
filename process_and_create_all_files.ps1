# Process all Vanilla Expanded items and create files
$json = Get-Content "F:\Python Apps\EPIC\vanilla_expanded_complete.json" | ConvertFrom-Json

# Load projectile damage
$projectiles = @{}
$modDirs = @("1814383360","1989352844","2194472657","2329126791","2375692535","2419690698","2454918139","2454918552","2454918354","2826922787","2723801948")
foreach ($modID in $modDirs) {
    $modPath = "E:\Steam\steamapps\workshop\content\294100\$modID"
    foreach ($ver in @("1.6","1.5","1.4")) {
        $defsPath = "$modPath\$ver\Defs"
        if (Test-Path $defsPath) {
            Get-ChildItem $defsPath -Recurse -Filter "*.xml" | ForEach-Object {
                try {
                    $xml = [xml](Get-Content $_.FullName)
                    foreach ($def in $xml.Defs.ThingDef) {
                        if ($def.projectile -and $def.defName) {
                            $damage = 0
                            if ($def.projectile.damageAmountBase) {
                                $damage = [float]$def.projectile.damageAmountBase
                            }
                            $projectiles[$def.defName] = $damage
                        }
                    }
                } catch {}
            }
            break
        }
    }
}

# Convert Rimworld damage to AFF track (rough conversion)
function Convert-ToAFFDamageTrack {
    param($damage, $isVehicleScale = $false)
    
    if ($isVehicleScale) {
        # Vehicle scale weapons: higher damage
        if ($damage -le 10) { return @(3,4,5,5,6,7,9) }
        if ($damage -le 15) { return @(4,5,6,7,8,9,12) }
        if ($damage -le 20) { return @(4,5,6,7,8,10,13) }
        if ($damage -le 30) { return @(5,6,7,8,9,11,14) }
        if ($damage -le 40) { return @(5,6,7,8,9,11,15) }
        return @(6,7,8,9,10,12,16)
    }
    
    # Normal weapons
    if ($damage -le 5) { return @(1,2,2,3,3,4,5) }
    if ($damage -le 10) { return @(2,3,3,4,4,5,6) }
    if ($damage -le 15) { return @(2,3,4,4,5,6,7) }
    if ($damage -le 20) { return @(3,4,4,5,5,6,8) }
    if ($damage -le 25) { return @(3,4,5,5,6,7,9) }
    if ($damage -le 30) { return @(3,4,5,6,7,8,10) }
    return @(4,5,6,7,8,9,11)
}

# Convert Rimworld armor (0-1.0 percentage) to AFF protection track
function Convert-ToAFFProtectionTrack {
    param($sharpArmor, $bluntArmor, $heatArmor)
    
    # Use the highest armor value
    $maxArmor = [Math]::Max($sharpArmor, [Math]::Max($bluntArmor, $heatArmor))
    
    # Convert percentage to 0-7 track
    if ($maxArmor -le 0.1) { return @(0,0,0,0,0,0,1) }
    if ($maxArmor -le 0.2) { return @(0,0,0,0,0,1,1) }
    if ($maxArmor -le 0.3) { return @(0,0,0,0,1,1,2) }
    if ($maxArmor -le 0.4) { return @(0,0,0,1,1,2,2) }
    if ($maxArmor -le 0.5) { return @(0,0,1,1,2,2,3) }
    if ($maxArmor -le 0.6) { return @(0,1,1,2,2,3,3) }
    if ($maxArmor -le 0.7) { return @(0,1,1,2,2,3,4) }
    if ($maxArmor -le 0.8) { return @(1,1,2,2,3,4,5) }
    return @(1,2,2,3,3,4,5)
}

Write-Host "Processing weapons and creating files..."
$weaponCount = 0

# Process weapons (this will be done in batches due to size)
$processedWeapons = @()
foreach ($weapon in $json.weapons) {
    # Get projectile damage if ranged
    if (-not $weapon.isMelee -and $weapon.projectileDef) {
        if ($projectiles.ContainsKey($weapon.projectileDef)) {
            $weapon.damage = $projectiles[$weapon.projectileDef]
            if ($weapon.cooldown -gt 0) {
                $weapon.dps = $weapon.damage / $weapon.cooldown
            }
        }
    }
    
    # Determine if vehicle scale (warcasket weapons)
    $isVehicleScale = $weapon.defName -like "*Warcasket*"
    
    # Convert to AFF track
    $affTrack = Convert-ToAFFDamageTrack $weapon.damage $isVehicleScale
    
    $weapon | Add-Member -NotePropertyName "affDamageTrack" -NotePropertyValue $affTrack
    $processedWeapons += $weapon
    $weaponCount++
    
    if ($weaponCount % 10 -eq 0) {
        Write-Host "Processed $weaponCount weapons..."
    }
}

Write-Host "Total weapons processed: $weaponCount"

# Save processed data
$processed = @{
    weapons = $processedWeapons
    armors = $json.armors
} | ConvertTo-Json -Depth 10

$processed | Out-File "F:\Python Apps\EPIC\vanilla_expanded_processed.json" -Encoding UTF8

Write-Host "Processing complete! Processed data saved."



