# Maplog manual representative-only decision

Woojin confirmed a product-direction correction for Maplog photo cover selection:

- The user manually chooses only one representative photo per Gathering.
- Rear/layer photos required by the 1/2/3-photo map-pin tiers are automatic Maplog selections, not user-editable slots.
- Entering `다른 사진으로 할래요` returns the existing automatic preview cards to the hand fan with no selected/lifted/slot state.
- Only the card the user taps or scrub-commits becomes visibly lifted as the manual representative. Selecting another card returns the previous representative to the fan.
- The automatic rear choices should feel uncurated but be deterministic for the same inputs, stable across re-entry/relaunch, and recompute after photo add/delete while retaining a valid manual representative.
- Existing user-selected full cover order is superseded; migration should interpret only the first legacy user cover as the manual representative and regenerate rear layers automatically.

This is user-confirmed and supersedes earlier implementation decisions that exposed multiple cover slots or preserved a user-selected complete cover order.
