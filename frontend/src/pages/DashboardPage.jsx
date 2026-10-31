import { useQuery } from '@tanstack/react-query';
import { Activity, BarChart3, MessageSquareText, PencilLine, ShieldCheck } from 'lucide-react';
import { Navigate } from 'react-router-dom';
import api from '../api/axios';
import { useAuth } from '../context/AuthContext';

export default function DashboardPage() {
  const { isOwner, loading } = useAuth();

  const { data, isLoading, isError } = useQuery({
    queryKey: ['dashboard-stats'],
    queryFn: () => api.get('/dashboard/stats/').then((res) => res.data),
    enabled: isOwner,
  });

  if (loading) return <div className="page-shell section-block state-card">Preparing dashboard...</div>;
  if (!isOwner) return <Navigate to="/login" replace />;

  const stats = [
    { label: 'Published posts', value: data?.published_posts ?? 0, icon: <PencilLine size={18} /> },
    { label: 'Total projects', value: data?.total_projects ?? 0, icon: <BarChart3 size={18} /> },
    { label: 'Comments', value: data?.total_comments ?? 0, icon: <MessageSquareText size={18} /> },
    { label: 'Unread messages', value: data?.unread_messages ?? 0, icon: <ShieldCheck size={18} /> },
  ];

  return (
    <div className="page-shell section-block dashboard-page">
      <div className="section-head">
        <p className="eyebrow">Dashboard</p>
        <h3>Portfolio overview</h3>
      </div>

      {isLoading && <div className="state-card">Loading stats...</div>}
      {isError && <div className="state-card error">Could not load dashboard metrics.</div>}

      {!isLoading && !isError && (
        <>
          <div className="stats-grid">
            {stats.map((stat) => (
              <div key={stat.label} className="stat-card">
                <div className="stat-icon">{stat.icon}</div>
                <div>
                  <strong>{stat.value}</strong>
                  <span>{stat.label}</span>
                </div>
              </div>
            ))}
          </div>

          <div className="dashboard-panels">
            <div className="panel-card">
              <h4>Top posts</h4>
              <ul className="list-panel">
                {(data?.top_posts ?? []).map((post) => (
                  <li key={post.slug}>
                    <span>{post.title}</span>
                    <small>{post.views_count} views</small>
                  </li>
                ))}
              </ul>
            </div>

            <div className="panel-card">
              <h4>Recent comments</h4>
              <ul className="list-panel">
                {(data?.recent_comments ?? []).map((comment) => (
                  <li key={comment.id}>
                    <span>{comment.name}</span>
                    <small>{comment.content.slice(0, 55)}{comment.content.length > 55 ? '…' : ''}</small>
                  </li>
                ))}
              </ul>
            </div>
          </div>

          <div className="panel-card">
            <h4>Operational snapshot</h4>
            <div className="mini-grid">
              <div><span>Total likes</span><strong>{data?.total_likes ?? 0}</strong></div>
              <div><span>Total views</span><strong>{data?.total_views ?? 0}</strong></div>
              <div><span>Draft posts</span><strong>{data?.draft_posts ?? 0}</strong></div>
              <div><span>Pending comments</span><strong>{data?.pending_comments ?? 0}</strong></div>
            </div>
          </div>
        </>
      )}
    </div>
  );
}
