'use client';
import { useState } from 'react';
import { useRouter } from 'next/navigation';

export default function NewPost() {
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await fetch('http://localhost:8000/api/posts/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          // Add JWT token here if authenticated
        },
        body: JSON.stringify({
          title,
          content,
          published: false, // Pending admin approval
        }),
      });
      if (!response.ok) throw new Error('Failed to submit post');
      router.push('/community');
    } catch (err) {
      setError((err as Error).message);
    }
  };

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <h1 className="text-4xl font-bold text-gray-800 mb-6">Share Your Story</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="title" className="block text-gray-700">Title</label>
          <input
            id="title"
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="w-full p-2 border rounded"
            required
          />
        </div>
        <div>
          <label htmlFor="content" className="block text-gray-700">Your Experience</label>
          <textarea
            id="content"
            value={content}
            onChange={(e) => setContent(e.target.value)}
            className="w-full p-2 border rounded"
            rows={5}
            required
          />
        </div>
        {error && <p className="text-red-600">{error}</p>}
        <button type="submit" className="px-6 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600">
          Submit
        </button>
      </form>
    </div>
  );
}