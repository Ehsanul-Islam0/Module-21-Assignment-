import { useQuery } from '@tanstack/react-query';
import { ExternalLink } from 'lucide-react';
import { Link, useParams } from 'react-router-dom';
import api from '../api/axios';

export default function ProjectDetailPage() {
  const { slug } = useParams();
  const { data, isLoading, isError } = useQuery({
    queryKey: ['project', slug],
    queryFn: () => api.get(`/projects/${slug}/`).then((res) => res.data),
  });

  if (isLoading) return <div className="page-shell section-block state-card">Loading project...</div>;
  if (isError || !data) return <div className="page-shell section-block state-card">Project could not be loaded.</div>;

  return (
    <div className="page-shell section-block project-detail">
      <div className="project-detail-banner" style={{ backgroundImage: `url(${data.cover_image || 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=1200&q=80'})` }} />
      <div className="project-detail-header">
        <div>
          <p className="eyebrow">Project</p>
          <h3>{data.title}</h3>
        </div>
        <div className="inline-links">
          {data.live_url && <a href={data.live_url} target="_blank" rel="noreferrer" className="button button-primary">Live demo <ExternalLink size={14} /></a>}
          {data.github_url && <a href={data.github_url} target="_blank" rel="noreferrer" className="button button-ghost">GitHub</a>}
        </div>
      </div>
      <p className="lead">{data.summary}</p>
      <p>{data.description}</p>
      <div className="tag-list">
        {data.tech_stack?.map((tech) => <span key={tech.id || tech} className="tag-pill">{typeof tech === 'object' ? tech.name : tech}</span>)}
      </div>
      <Link to="/projects" className="text-link">← Back to projects</Link>
    </div>
  );
}
