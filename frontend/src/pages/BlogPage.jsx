import { useMemo, useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Search } from 'lucide-react';
import { Link } from 'react-router-dom';
import api from '../api/axios';

const listFrom = (data) => (Array.isArray(data) ? data : data?.results || []);

export default function BlogPage() {
  const [search, setSearch] = useState('');
  const params = useMemo(() => ({ search: search || undefined }), [search]);
  const { data: categoriesData } = useQuery({ queryKey: ['categories'], queryFn: () => api.get('/categories/').then((res) => res.data) });
  const { data: postsData, isLoading, isError, refetch } = useQuery({
    queryKey: ['posts', params],
    queryFn: () => api.get('/posts/', { params }).then((res) => res.data),
  });

  const categories = listFrom(categoriesData);
  const posts = listFrom(postsData);

  return (
    <div className="page-shell section-block">
      <div className="section-head">
        <p className="eyebrow">Blog</p>
        <h3>Product thinking, engineering notes, and lessons learned</h3>
      </div>

      <div className="toolbar stack-toolbar">
        <div className="search-box"><Search size={16} /><input value={search} onChange={(e) => setSearch(e.target.value)} placeholder="Search articles" /></div>
        <div className="chip-row">
          {categories.map((category) => (
            <button key={category.id} className="chip" type="button">{category.name}</button>
          ))}
        </div>
      </div>

      {isLoading && <div className="state-card">Loading posts...</div>}
      {isError && <div className="state-card error">Could not load posts. <button className="button button-ghost" onClick={() => refetch()}>Retry</button></div>}
      {!isLoading && !isError && posts.length === 0 && <div className="state-card">No posts found for this search.</div>}

      <div className="card-grid blog-grid">
        {posts.map((post) => (
          <Link key={post.id} to={`/blog/${post.slug}`} className="blog-card">
            <div className="blog-card-image" style={{ backgroundImage: `url(${post.cover_image || 'https://images.unsplash.com/photo-1498050108023-c5249f4df085?auto=format&fit=crop&w=1200&q=80'})` }} />
            <div className="blog-card-body">
              <span className="tag-pill">{post.category}</span>
              <h4>{post.title}</h4>
              <p>{post.excerpt}</p>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}
