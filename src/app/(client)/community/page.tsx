'use client';
import { useState, useEffect } from 'react';
import Link from 'next/link';
import api from '@/lib/api';

interface Post {
  id: number;
  title: string;
  slug: string;
  content: string;
  published: boolean;
}


interface PaginatedPosts {
    count: number;
    next: string | null;
    previous: string | null;
    results: Post[];
  }


export default function Community() {
  const [posts, setPosts] = useState<Post[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchArticles = async () => {
      try {
        // Use the axios instance:
        const response = await api.get<PaginatedPosts>("/posts");
        console.log('API response:', response.data);
        // Axios returns data in response.data
        setPosts(response.data.results);
      } catch (err) {
        setError((err as Error).message);
      } finally {
        setLoading(false);
      }
    };

    fetchArticles();
  }, []);

  if (loading) return <p className="p-6 text-gray-600">Loading community posts...</p>;
  if (error) return <p className="p-6 text-red-600">Error: {error}</p>;

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <h1 className="text-4xl font-bold text-gray-800 mb-6">Community</h1>
      <p className="text-gray-600 mb-4">Share your experiences or ask questions about chronic pain management.</p>
      <Link href="/community/new" className="inline-block mb-6 px-6 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600">
        Share Your Story
      </Link>
      {posts.length === 0 ? (
        <p className="text-gray-600">No community posts yet—be the first to share!</p>
      ) : (
        <div className="space-y-6">
          {posts.map((post) => (
            <div key={post.id} className="p-4 bg-white rounded-lg shadow-md">
              <h2 className="text-2xl font-semibold text-blue-600">{post.title}</h2>
              <p className="text-gray-600 mt-2">{post.content.slice(0, 100) + '...'}</p>
              <Link href={`/community/${post.slug}`} className="text-blue-500 hover:underline mt-2 inline-block">
                Read More
              </Link>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}