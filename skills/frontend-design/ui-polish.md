# Product UI Polish

Use this guide for product interfaces such as dashboards, forms, settings, tools, games, and application screens. Improve the product's hierarchy and interaction quality without imposing a house style.

## Read the Product First

For an existing product, inspect the current rendered surface, one or two nearby screens, real content, design tokens, and project-local `DESIGN.md`. Preserve established identity and interaction contracts unless the user asked for a redesign.

For a new product, infer one coherent visual direction from audience, task frequency, content density, platform, and brand. Treat the direction as a hypothesis that the rendered result can disprove.

## Durable Quality Bar

- **Hierarchy:** the most important content and next action are easy to find.
- **States:** relevant loading, empty, partial, success, error, permission, disabled, and recovery states are designed.
- **Accessibility:** semantics, focus, contrast, touch targets, text scaling, reduced motion, and input modality fit the platform.
- **Responsiveness:** real content, long labels, small screens, and large screens do not break the composition.
- **Consistency:** repeated elements share intentional tokens and behavior.
- **Platform fit:** use native or established project patterns when they provide better behavior and feel.

## Visual Judgment

Avoid generic output by making decisions from the product, not by banning particular styles.

- Reuse existing type, spacing, color, radius, elevation, icon, and motion systems when they work.
- Change a token or pattern when the current artifact shows a concrete hierarchy, legibility, interaction, or identity problem.
- System fonts, symmetry, cards, glass, gradients, dense layouts, or quiet minimalism may all be correct in context.
- Prefer a small number of intentional relationships over arbitrary limits on font sizes, colors, radii, or durations.
- Let content and platform needs decide whether the interface should feel quiet, expressive, dense, playful, editorial, or utilitarian.

If Tailwind or another utility system is present, use project tokens rather than accidentally inheriting framework defaults. Do not create a new token system for a local polish task.

## Work and Verify

1. Identify the user-facing weakness and the product evidence behind it.
2. Choose one direction that fits the product; briefly compare alternatives only when the choice matters.
3. Implement the smallest coherent change that resolves the weakness across relevant states.
4. Inspect the rendered result and the interactions affected by the change.
5. Read visible copy as the intended user and remove request wording, design rationale, production notes, or workflow residue that does not belong in the product.
6. Revise any choice that looks correct in code but fails with real content or at a target viewport.

Report the user-facing change, the reason for the chosen direction, observed verification, and remaining uncertainty. Do not emit a design-spec template unless requested.
