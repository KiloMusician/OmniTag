# Godot 4.1 atlas offsets: context-preserving handoff

[Msg⛛{GODOT41-ATLAS-OFFSET-20261021}] [State⛛{Documented}] [Ctx⛛{HistoricalSessionHandoff}]

## Origin
A previous session asked where the old TileSet "offset" control went in Godot 4.1, and whether atlas **Margins** or **Separation** was the equivalent. This is a narrowly scoped knowledge handoff, not a claim about the current game projects' engine versions or build health.

## Correct distinction
- **Margins** (`TileSetAtlasSource.margins`) is the empty pixel border from the texture's top-left edges before the first atlas cell. Use it when the source spritesheet has an outer border.
- **Separation** (`TileSetAtlasSource.separation`) is the pixel gap between atlas cells. Use it for evenly spaced padding between sprites.
- **Texture region size** (`TileSetAtlasSource.texture_region_size`) sets the dimensions of an atlas grid cell.
- **Texture origin** (`TileData.texture_origin`) shifts the *rendered appearance* of a tile relative to its map cell. This is the closer match for an individual tile's drawing offset, and is **not** replaced by atlas margins or separation.
- The prompt to automatically create tiles in non-transparent regions is an atlas tile-creation convenience; it does not choose a rendering offset.

## Example
For a 16×16 sprite grid with a 2px outer border and 1px gap between cells:
`texture_region_size = Vector2i(16,16)`
`margins = Vector2i(2,2)`
`separation = Vector2i(1,1)`

For a tile that needs to render 4px higher than its logical map position, adjust that tile's **Texture Origin** instead (verify sign in editor).

## Safe integration
1. Check the actual Godot version in each project before applying the advice.
2. Verify spritesheet pixel dimensions and the atlas grid before changing resources.
3. Keep texture sampling/bleeding issues distinct from positioning problems.
4. Test changes in the editor and in an actual playtest, not solely via a headless import.
5. Treat this as documentation only: no runtime files or tilesets were modified or tested.

## Colony re-engagement context
A 2026-10-21 operator directive requested context-gap analysis before modifications: inspect branch, status, recent commits, dependency manifests, issues, CI and build health; do not discard WIP, override human gates, or claim a fleet is healthy without probing it. This handoff deliberately avoids duplicating the colony's operational authority or asserting access to the local rig.

[State⛛{UnverifiedRuntime}] [Act⛛{DocumentOnly}]
