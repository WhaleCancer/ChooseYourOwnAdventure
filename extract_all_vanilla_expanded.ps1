# Comprehensive extraction of all Vanilla Expanded weapons and armor
$workshopDir = "E:\Steam\steamapps\workshop\content\294100"
$outputFile = "F:\Python Apps\EPIC\vanilla_expanded_complete.json"

$allWeapons = @()
$allArmors = @()

# All Vanilla Expanded mods to scan
$vweMods = @{
    "1814383360" = "Vanilla Weapons Expanded"
    "1989352844" = "Vanilla Weapons Expanded - Laser"
    "2194472657" = "Vanilla Weapons Expanded - Grenades"
    "2329126791" = "Vanilla Weapons Expanded - Heavy Weapons"
    "2375692535" = "Vanilla Weapons Expanded - Coilguns"
    "2419690698" = "Vanilla Weapons Expanded - Makeshift"
    "2454918139" = "Vanilla Weapons Expanded - Frontier"
    "2454918552" = "Vanilla Weapons Expanded - Non-Lethal"
    "2454918354" = "Vanilla Weapons Expanded - Tribal"
    "2826922787" = "Vanilla Persona Weapons Expanded"
}

$vaeMods = @{
    "1814988282" = "Vanilla Armour Expanded"
    "1814987817" = "Vanilla Apparel Expanded"
    "2521176396" = "Vanilla Apparel Expanded - Accessories"
}

$vfeMods = @{
    "2052918119" = "Vanilla Factions Expanded - Settlers"
    "2654846754" = "Vanilla Factions Expanded - Ancients"
    "2723801948" = "Vanilla Factions Expanded - Pirates"
    "2787850474" = "Vanilla Factions Expanded - Classical"
}

function Extract-WeaponData {
    param($def, $modName, $modID)
    
    $weapon = @{
        defName = $def.defName
        label = $def.label
        description = $def.description
        techLevel = $def.techLevel
        mod = $modName
        modID = $modID
        isMelee = $false
        damage = 0
        dps = 0
        cooldown = 0
        range = 0
        mass = 0
        projectileDef = $null
    }
    
    # Check if melee (has tools)
    if ($def.tools) {
        $weapon.isMelee = $true
        # Extract tool power (damage) and cooldown
        $maxPower = 0
        $maxCooldown = 0
        foreach ($tool in $def.tools.GetElementsByTagName("li")) {
            if ($tool.power) { $power = [float]$tool.power; if ($power -gt $maxPower) { $maxPower = $power } }
            if ($tool.cooldownTime) { $cooldown = [float]$tool.cooldownTime; if ($cooldown -gt $maxCooldown) { $maxCooldown = $cooldown } }
        }
        $weapon.damage = $maxPower
        $weapon.cooldown = $maxCooldown
        if ($maxCooldown -gt 0) { $weapon.dps = $maxPower / $maxCooldown }
    }
    
    # Check if ranged (has verbs with projectiles)
    if ($def.verbs) {
        foreach ($verb in $def.verbs.GetElementsByTagName("li")) {
            if ($verb.defaultProjectile) {
                $weapon.isMelee = $false
                $weapon.projectileDef = $verb.defaultProjectile
                if ($verb.range) { $weapon.range = [float]$verb.range }
            }
        }
    }
    
    # Extract stats
    if ($def.statBases) {
        if ($def.statBases.RangedWeapon_Cooldown) { $weapon.cooldown = [float]$def.statBases.RangedWeapon_Cooldown }
        if ($def.statBases.MeleeWeapon_AverageDPS) { $weapon.dps = [float]$def.statBases.MeleeWeapon_AverageDPS }
        if ($def.statBases.Mass) { $weapon.mass = [float]$def.statBases.Mass }
    }
    
    return $weapon
}

function Extract-ArmorData {
    param($def, $modName, $modID)
    
    $armor = @{
        defName = $def.defName
        label = $def.label
        description = $def.description
        techLevel = $def.techLevel
        mod = $modName
        modID = $modID
        sharpArmor = 0
        bluntArmor = 0
        heatArmor = 0
        mass = 0
        bodyPartGroups = @()
        layers = @()
    }
    
    # Extract armor stats
    if ($def.statBases) {
        if ($def.statBases.ArmorRating_Sharp) { $armor.sharpArmor = [float]$def.statBases.ArmorRating_Sharp }
        if ($def.statBases.ArmorRating_Blunt) { $armor.bluntArmor = [float]$def.statBases.ArmorRating_Blunt }
        if ($def.statBases.ArmorRating_Heat) { $armor.heatArmor = [float]$def.statBases.ArmorRating_Heat }
        if ($def.statBases.Mass) { $armor.mass = [float]$def.statBases.Mass }
    }
    
    # Extract body parts and layers
    if ($def.apparel) {
        if ($def.apparel.bodyPartGroups) {
            foreach ($bp in $def.apparel.bodyPartGroups.GetElementsByTagName("li")) {
                $armor.bodyPartGroups += $bp.InnerText
            }
        }
        if ($def.apparel.layers) {
            foreach ($layer in $def.apparel.layers.GetElementsByTagName("li")) {
                $armor.layers += $layer.InnerText
            }
        }
    }
    
    return $armor
}

# Process all mods
$allMods = $vweMods + $vaeMods + $vfeMods

foreach ($kvp in $allMods.GetEnumerator()) {
    $modID = $kvp.Key
    $modName = $kvp.Value
    $modPath = Join-Path $workshopDir $modID
    
    if (-not (Test-Path $modPath)) { continue }
    
    Write-Host "Processing $modName ($modID)..."
    
    # Find latest version
    $versionDirs = @("1.6", "1.5", "1.4", "1.3")
    $defsPath = $null
    foreach ($ver in $versionDirs) {
        $testPath = Join-Path $modPath $ver
        if (Test-Path $testPath) {
            $defsPath = Join-Path $testPath "Defs"
            if (Test-Path $defsPath) { break }
        }
    }
    
    if (-not $defsPath) { continue }
    
    # Scan all XML files
    $xmlFiles = Get-ChildItem $defsPath -Recurse -Filter "*.xml" -ErrorAction SilentlyContinue
    foreach ($xmlFile in $xmlFiles) {
        try {
            $xml = [xml](Get-Content $xmlFile.FullName -ErrorAction Stop)
            foreach ($def in $xml.Defs.ThingDef) {
                if (-not $def.defName) { continue }
                
                # Check if weapon
                $isWeapon = ($def.tools -ne $null) -or ($def.verbs -ne $null) -or 
                           ($def.ParentName -like "*Weapon*") -or 
                           ($def.defName -like "*Gun*") -or 
                           ($def.defName -like "*Weapon*")
                
                # Check if armor/apparel
                $isArmor = ($def.apparel -ne $null) -or 
                          ($def.ParentName -like "*Apparel*") -or 
                          ($def.defName -like "*Armor*") -or
                          ($def.defName -like "*Apparel*")
                
                # Exclude projectiles, bullets, etc.
                $exclude = ($def.defName -like "*Projectile*") -or 
                          ($def.defName -like "*Bullet*") -or
                          ($def.defName -like "*Arrow*") -or
                          ($def.defName -like "*Gas*")
                
                if ($exclude) { continue }
                
                if ($isWeapon) {
                    $weapon = Extract-WeaponData $def $modName $modID
                    $allWeapons += $weapon
                }
                
                if ($isArmor) {
                    $armor = Extract-ArmorData $def $modName $modID
                    $allArmors += $armor
                }
            }
        } catch {
            # Skip files that can't be parsed
        }
    }
}

# Output results
$output = @{
    weapons = $allWeapons
    armors = $allArmors
} | ConvertTo-Json -Depth 10

$output | Out-File $outputFile -Encoding UTF8

Write-Host "`nExtraction complete!"
Write-Host "Found $($allWeapons.Count) weapons"
Write-Host "Found $($allArmors.Count) armor/apparel items"
Write-Host "Results saved to $outputFile"



