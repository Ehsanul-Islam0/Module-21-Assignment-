import { useQuery } from '@tanstack/react-query';
import api from '../api/axios';

const listFrom = (data) => (Array.isArray(data) ? data : data?.results || []);

export default function AboutPage() {
  const { data: profile } = useQuery({ queryKey: ['profile'], queryFn: () => api.get('/profile/').then((res) => res.data) });
  const { data: experiences } = useQuery({ queryKey: ['experiences'], queryFn: () => api.get('/experiences/').then((res) => res.data) });
  const { data: education } = useQuery({ queryKey: ['education'], queryFn: () => api.get('/education/').then((res) => res.data) });

  return (
    <div className="page-shell section-block">
      <div className="section-head">
        <p className="eyebrow">About</p>
        <h3>Building software that feels thoughtful and helps real people</h3>
      </div>
      <div className="about-layout">
        <div>
          <p className="lead">{profile?.bio || 'I create products that balance clarity, speed, and maintainability.'}</p>
          <div className="info-list">
            <p><strong>Email:</strong> {profile?.email}</p>
            <p><strong>Location:</strong> {profile?.location}</p>
            <p><strong>Experience:</strong> {profile?.years_of_experience || 2}+ years</p>
          </div>
        </div>
        <div className="portrait-card">
          <img src="https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&w=900&q=80" alt="Md Ehsanul Islam" />
        </div>
      </div>

      <div className="split-columns">
        <div>
          <h4>Experience</h4>
          {listFrom(experiences).map((item) => (
            <div key={item.id} className="timeline-item compact">
              <span className="timeline-dot" />
              <div>
                <h5>{item.role}</h5>
                <p>{item.company} • {item.location}</p>
                <small>{item.start_date} to {item.is_current ? 'Present' : item.end_date}</small>
              </div>
            </div>
          ))}
        </div>

        <div>
          <h4>Education</h4>
          {listFrom(education).map((item) => (
            <div key={item.id} className="timeline-item compact">
              <span className="timeline-dot" />
              <div>
                <h5>{item.degree}</h5>
                <p>{item.institution}</p>
                <small>{item.start_year}–{item.end_year || 'Present'}</small>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
