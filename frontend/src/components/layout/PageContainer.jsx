export default function PageContainer({ children, as = 'div' }) {
  const Component = as;
  return <Component className="page-shell">{children}</Component>;
}
