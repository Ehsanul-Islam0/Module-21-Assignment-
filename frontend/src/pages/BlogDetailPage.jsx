import { useState } from 'react';
import { useMutation, useQuery } from '@tanstack/react-query';
import { Heart, MessageSquare, Share2 } from 'lucide-react';
import { useParams } from 'react-router-dom';
import api from '../api/axios';

export default function BlogDetailPage() {
  const { slug } = useParams();
  const [comment, setComment] = useState({ name: '', email: '', content: '' });
  const [commentFeedback, setCommentFeedback] = useState('');
  const [liked, setLiked] = useState(false);
  const [likeCount, setLikeCount] = useState(0);

  const { data, isLoading, isError } = useQuery({
    queryKey: ['post', slug],
    queryFn: () => api.get(`/posts/${slug}/`).then((res) => res.data),
    onSuccess: (post) => {
      setLiked(Boolean(post.is_liked));
      setLikeCount(post.likes_count || 0);
    },
  });

  const { data: comments } = useQuery({
    queryKey: ['post-comments', slug],
    queryFn: () => api.get(`/posts/${slug}/comments/`).then((res) => res.data),
  });

  const toggleLike = useMutation({
    mutationFn: async () => {
      const visitorId = localStorage.getItem('visitorId') || crypto.randomUUID();
      localStorage.setItem('visitorId', visitorId);
      const response = await api.post(`/posts/${slug}/like/`, {}, { headers: { 'X-Visitor-Id': visitorId } });
      return response.data;
    },
    onSuccess: (payload) => {
      setLiked(payload.liked);
      setLikeCount(payload.likes_count);
    },
  });

  const postComment = useMutation({
    mutationFn: async () => {
      const response = await api.post(`/posts/${slug}/comments/`, comment);
      return response.data;
    },
    onSuccess: (payload) => {
      setCommentFeedback(payload.message || 'Your comment is awaiting approval.');
      setComment({ name: '', email: '', content: '' });
    },
  });

  const handleCommentSubmit = (e) => {
    e.preventDefault();
    postComment.mutate();
  };

  if (isLoading) return <div className="page-shell section-block state-card">Loading post...</div>;
  if (isError || !data) return <div className="page-shell section-block state-card">This post could not be loaded.</div>;

  return (
    <article className="page-shell section-block post-detail">
      <div className="post-hero" style={{ backgroundImage: `url(${data.cover_image || 'https://images.unsplash.com/photo-1498050108023-c5249f4df085?auto=format&fit=crop&w=1200&q=80'})` }} />
      <div className="meta-row">
        <span>{data.category?.name || data.category}</span>
        <span>{new Date(data.published_at).toLocaleDateString()}</span>
        <span>{data.reading_time || 4} min read</span>
        <span>{data.views_count || 0} views</span>
      </div>
      <h3>{data.title}</h3>
      <div className="tag-list">{(data.tags || []).map((tag) => <span key={tag.slug || tag.id} className="tag-pill">{tag.name || tag}</span>)}</div>
      <div className="post-content" dangerouslySetInnerHTML={{ __html: data.content || '' }} />

      <div className="post-actions">
        <button className="button button-ghost" onClick={() => toggleLike.mutate()}><Heart size={16} fill={liked ? 'currentColor' : 'none'} /> {likeCount} likes</button>
        <button className="button button-ghost"><Share2 size={16} /> Share</button>
      </div>

      <div className="comment-section">
        <h4><MessageSquare size={16} /> Comments</h4>
        <form className="comment-form" onSubmit={handleCommentSubmit}>
          <input value={comment.name} onChange={(e) => setComment({ ...comment, name: e.target.value })} placeholder="Your name" required />
          <input value={comment.email} onChange={(e) => setComment({ ...comment, email: e.target.value })} type="email" placeholder="Your email" required />
          <textarea value={comment.content} onChange={(e) => setComment({ ...comment, content: e.target.value })} placeholder="Write a comment" required rows={5} />
          <button className="button button-primary" type="submit" disabled={postComment.isPending}>Post comment</button>
        </form>
        {commentFeedback && <p className="form-message">{commentFeedback}</p>}

        <div className="comments-list">
          {(comments || []).map((commentItem) => (
            <div key={commentItem.id} className="comment-item">
              <h5>{commentItem.name}</h5>
              <p>{commentItem.content}</p>
            </div>
          ))}
        </div>
      </div>
    </article>
  );
}
