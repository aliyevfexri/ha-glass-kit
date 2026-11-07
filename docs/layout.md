# Laying out a dashboard with the kit

- **One `sections` view** per screen, `theme: glass`, `max_columns` 2–3. Sections reflow: phone = one column, tablet/laptop = side by side. No fixed pixel layouts.
- **Header chips** = core view `badges` with `visibility` conditions: they appear only when something needs attention (washer finished, door open, boiler on). No chips = nothing to worry about.
- **Sections in priority order**: the thing people use most first (e.g. heating), then rooms, then appliances. On a phone this is the scroll order.
- **Pop-ups** (bubble-card `pop-up` with a `hash`) for detail and rarely used controls; tiles navigate to them. The main screen stays read-at-a-glance.
- **Footer** (bubble-card `horizontal-buttons-stack`): links to pop-ups, same on every view. The bar is fixed over the page: end the view with a full-width section (`column_span` = max_columns) holding the footer and a `kit_spacer`, or the last row stays hidden behind the bar.
- **Fixed layout**: tiles don't move by themselves; layout changes are made in YAML and reviewed.
- Keep one page. Add a second view only when the first one no longer fits a tablet screen without scrolling.
