export default function Footer() {
  return (
    <footer className="site-footer">
      <div className="page-shell footer-grid">
        <div>
          <h3>Md Ehsanul Islam</h3>
          <p>Full-stack developer crafting reliable interfaces and resilient backend systems.</p>
        </div>
        <div>
          <h4>Quick links</h4>
          <ul>
            <li><a href="/about">About</a></li>
            <li><a href="/projects">Projects</a></li>
            <li><a href="/blog">Blog</a></li>
            <li><a href="/contact">Contact</a></li>
          </ul>
        </div>
        <div>
          <h4>Social</h4>
          <ul>
            <li><a href="https://github.com" target="_blank" rel="noreferrer">GitHub</a></li>
            <li><a href="https://linkedin.com" target="_blank" rel="noreferrer">LinkedIn</a></li>
            <li><a href="https://x.com" target="_blank" rel="noreferrer">X</a></li>
          </ul>
        </div>
      </div>
      <div className="copyright">© {new Date().getFullYear()} Md Ehsanul Islam. All rights reserved.</div>
    </footer>
  );
}
