// Runtime inventory for correlating the CurseForge manifest with actual loaded
// mod IDs. The generated file is intentionally ignored by Git and can be sent
// back as validation evidence after a normal client startup.

var InventoryFiles = Java.loadClass('java.nio.file.Files')
var InventoryPaths = Java.loadClass('java.nio.file.Paths')
var InventoryStandardCharsets = Java.loadClass('java.nio.charset.StandardCharsets')

function inventoryString(value) {
  if (value == null) {
    return ''
  }
  try {
    return String(value)
  } catch (error) {
    return ''
  }
}

function inventoryValue(mod, property) {
  try {
    return inventoryString(mod[property])
  } catch (error) {
    return ''
  }
}

function exportLoadedModInventory() {
  var ids = Object.keys(Platform.mods).sort()
  var projects = ids.map(function(modId) {
    var mod = Platform.mods[modId]
    return {
      mod_id: modId,
      name: inventoryValue(mod, 'name'),
      version: inventoryValue(mod, 'version')
    }
  })

  var document = {
    schema_version: 1,
    minecraft_version: inventoryString(Platform.minecraftVersion),
    loaded_mod_count: projects.length,
    projects: projects
  }

  try {
    var directory = InventoryPaths.get('kubejs', 'exported')
    InventoryFiles.createDirectories(directory)
    var output = directory.resolve('expert_loaded_mods.json')
    InventoryFiles.writeString(
      output,
      JSON.stringify(document, null, 2) + '\n',
      InventoryStandardCharsets.UTF_8
    )
    console.info('[ModInventory] Exported ' + projects.length + ' loaded mods to ' + output)
  } catch (error) {
    console.error('[ModInventory] Failed to export loaded mod inventory: ' + error)
  }
}

exportLoadedModInventory()
