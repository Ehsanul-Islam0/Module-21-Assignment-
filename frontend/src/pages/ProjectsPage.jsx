import { useMemo, useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { ExternalLink, Search } from 'lucide-react';
import { Link } from 'react-router-dom';
import api from '../api/axios';

const listFrom = (data) => (Array.isArray(data) ? data : data?.results || []);

export default function ProjectsPage() {
  const [search, setSearch] = useState('');
  const params = useMemo(() => ({ search: search || undefined }), [search]);
  const { data, isLoading, isError, refetch } = useQuery({
    queryKey: ['projects', params],
    queryFn: () => api.get('/projects/', { params }).then((res) => res.data),
  });

  const projects = listFrom(data);

  return (
    <div className="page-shell section-block">
      <div className="section-head">
        <p className="eyebrow">Projects</p>
        <h3>Product work that solves real problems</h3>
      </div>
      <div className="toolbar">
        <div className="search-box"><Search size={16} /><input value={search} onChange={(e) => setSearch(e.target.value)} placeholder="Search projects" /></div>
      </div>

      {isLoading && <div className="state-card">Loading projects...</div>}
      {isError && <div className="state-card error">Could not load projects. <button className="button button-ghost" onClick={() => refetch()}>Retry</button></div>}
      {!isLoading && !isError && projects.length === 0 && <div className="state-card">No projects found.</div>}

      <div className="card-grid project-grid">
        {projects.map((project) => (
          <Link key={project.id} to={`/projects/${project.slug}`} className="project-card large">
            <div className="project-image" style={{ backgroundImage: `url(${project.cover_image || 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=1200&q=80'})` }} />
            <div className="project-card-body">
              <h4>{project.title}</h4>
              <p>{project.summary}</p>
              <span className="inline-link">Open project <ExternalLink size={14} /></span>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}
