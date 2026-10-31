import { ArrowRight, Briefcase, Download, ExternalLink, Globe, Mail, MapPin } from 'lucide-react';
import { useQuery } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import api from '../api/axios';

const listFrom = (data) => (Array.isArray(data) ? data : data?.results || []);

export default function HomePage() {
  const { data: profile } = useQuery({ queryKey: ['profile'], queryFn: () => api.get('/profile/').then((res) => res.data) });
  const { data: projectsData } = useQuery({ queryKey: ['featured-projects'], queryFn: () => api.get('/projects/', { params: { is_featured: true, page: 1 } }).then((res) => res.data) });
  const { data: postsData } = useQuery({ queryKey: ['featured-posts'], queryFn: () => api.get('/posts/', { params: { is_featured: true, page: 1 } }).then((res) => res.data) });
  const skills = listFrom(useQuery({ queryKey: ['skills'], queryFn: () => api.get('/skills/').then((res) => res.data) }).data || []);

  const projects = listFrom(projectsData).slice(0, 3);
  const posts = listFrom(postsData).slice(0, 3);

  return (
    <>
      <section className="hero-section page-shell">
        <div className="hero-copy">
          <p className="eyebrow">Available for work</p>
          <h1>{profile?.full_name || 'Md Ehsanul Islam'}</h1>
          <h2>{profile?.headline || 'Full-Stack Developer'}</h2>
          <p className="lead">I design polished interfaces and build dependable backend systems that help real products ship with confidence.</p>
          <div className="hero-actions">
            <Link className="button button-primary" to="/projects">View Projects <ArrowRight size={16} /></Link>
            <a className="button button-ghost" href={profile?.resume || '#'} target="_blank" rel="noreferrer">Download Resume <Download size={16} /></a>
          </div>
          <div className="social-row">
            {profile?.github_url && <a href={profile.github_url} target="_blank" rel="noreferrer"><Globe size={18} /></a>}
            {profile?.linkedin_url && <a href={profile.linkedin_url} target="_blank" rel="noreferrer"><Briefcase size={18} /></a>}
            {profile?.email && <a href={`mailto:${profile.email}`}><Mail size={18} /></a>}
            {profile?.location && <span className="meta-pill"><MapPin size={14} /> {profile.location}</span>}
          </div>
        </div>
        <div className="hero-visual">
          <img src="https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&w=900&q=80" alt="Md Ehsanul Islam" />
        </div>
      </section>

      <section className="page-shell section-block">
        <div className="section-head">
          <p className="eyebrow">About</p>
          <h3>Product-minded developer with a strong technical foundation</h3>
        </div>
        <p className="section-text">{profile?.bio || 'I enjoy turning ideas into experiences that are measurable, maintainable, and easy to trust.'}</p>
        <Link to="/about" className="text-link">More about me →</Link>
      </section>

      <section className="page-shell section-block">
        <div className="section-head">
          <p className="eyebrow">Skills</p>
          <h3>Tools I use to build reliable products</h3>
        </div>
        <div className="skills-grid">
          {skills.slice(0, 10).map((skill) => (
            <div key={skill.id} className="skill-card">
              <div className="skill-topline">
                <span>{skill.name}</span>
                <span>{skill.proficiency}%</span>
              </div>
              <div className="progress-bar"><span style={{ width: `${skill.proficiency}%` }} /></div>
            </div>
          ))}
        </div>
      </section>

      <section className="page-shell section-block">
        <div className="section-head">
          <p className="eyebrow">Experience</p>
          <h3>Recent work and problem-solving</h3>
        </div>
        <div className="timeline-list">
          {listFrom(useQuery({ queryKey: ['experiences'], queryFn: () => api.get('/experiences/').then((res) => res.data) }).data || []).slice(0, 2).map((item) => (
            <div key={item.id} className="timeline-item">
              <span className="timeline-dot" />
              <div>
                <h4>{item.role}</h4>
                <p>{item.company} • {item.location}</p>
                <ul>
                  {item.description ? item.description.split('.').filter(Boolean).slice(0, 2).map((line) => <li key={line}>{line.trim()}</li>) : null}
                </ul>
              </div>
            </div>
          ))}
        </div>
      </section>

      <section className="page-shell section-block">
        <div className="section-head">
          <p className="eyebrow">Featured projects</p>
          <h3>Selected work</h3>
        </div>
        <div className="card-grid project-grid">
          {projects.map((project) => (
            <Link to={`/projects/${project.slug}`} key={project.id} className="project-card">
              <div className="project-image" style={{ backgroundImage: `url(${project.cover_image || 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=1200&q=80'})` }} />
              <div className="project-card-body">
                <h4>{project.title}</h4>
                <p>{project.summary}</p>
                <span className="inline-link">See project <ExternalLink size={14} /></span>
              </div>
            </Link>
          ))}
        </div>
        <div className="section-action"><Link to="/projects" className="text-link">See all projects →</Link></div>
      </section>

      <section className="page-shell section-block">
        <div className="section-head">
          <p className="eyebrow">Latest posts</p>
          <h3>Ideas, notes, and lessons</h3>
        </div>
        <div className="card-grid blog-grid">
          {posts.map((post) => (
            <Link to={`/blog/${post.slug}`} key={post.id} className="blog-card">
              <div className="blog-card-image" style={{ backgroundImage: `url(${post.cover_image || 'https://images.unsplash.com/photo-1498050108023-c5249f4df085?auto=format&fit=crop&w=1200&q=80'})` }} />
              <div className="blog-card-body">
                <span className="tag-pill">{post.category}</span>
                <h4>{post.title}</h4>
                <p>{post.excerpt}</p>
              </div>
            </Link>
          ))}
        </div>
        <div className="section-action"><Link to="/blog" className="text-link">Read the blog →</Link></div>
      </section>

      <section className="page-shell contact-cta">
        <h3>Let’s build something meaningful.</h3>
        <Link to="/contact" className="button button-primary">Get in touch</Link>
      </section>
    </>
  );
}
