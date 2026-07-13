# Component Template (Presenter)

```jsx
// OrderTable.jsx — presentation only, no fetching/store imports
export default function OrderTable({ rows, isLoading, error, onRowClick }) {
  if (error) return <ErrorState message={error.message} />;
  if (isLoading) return <SkeletonTable rows={5} />;
  if (rows.length === 0) return <EmptyState label="No orders yet" />;

  return (
    <table role="table" aria-label="Orders">
      <thead>...</thead>
      <tbody>
        {rows.map((r) => (
          <tr key={r.id} tabIndex={0} onClick={() => onRowClick(r.id)}
              onKeyDown={(e) => e.key === "Enter" && onRowClick(r.id)}>
            ...
          </tr>
        ))}
      </tbody>
    </table>
  );
}
```

```jsx
// useOrderTable.js — container: owns fetching + derived state
export function useOrderTable() {
  const { data, isLoading, error } = useQuery(["orders"], fetchOrders);
  const rows = useMemo(() => data?.map(toRow) ?? [], [data]);
  const onRowClick = useCallback((id) => navigate(`/orders/${id}`), []);
  return { rows, isLoading, error, onRowClick };
}
```

Loading, error, and empty states are explicit branches — never an implicit blank render.
