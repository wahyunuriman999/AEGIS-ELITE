# Compound Components

For widget families (Tabs, Select, Accordion, Menu) expose a set of components that share
implicit state via context, instead of one component with a wall of boolean/config props:

```jsx
<Tabs defaultValue="a">
  <Tabs.List>
    <Tabs.Trigger value="a">A</Tabs.Trigger>
    <Tabs.Trigger value="b">B</Tabs.Trigger>
  </Tabs.List>
  <Tabs.Panel value="a">...</Tabs.Panel>
</Tabs>
```

vs. `<Tabs items={[...]} renderItem={...} activeIndicatorPosition="..." ... />`. The compound
form scales to new layout requirements without new props — the caller controls composition
directly — and each sub-component stays small and independently testable. Cost: more files per
widget, and the pieces are only usable together (document that coupling in the widget's own
README, not implicitly).
