import { notFound } from 'next/navigation';

interface Post {
  id: number;
  title: string;
  slug: string;
  content: string;
  created_at: string;
}

export default async function PostPage({ params }: { params: { slug: string } }) {
  const response = await fetch(`http://localhost:8000/api/posts/?slug=${params.slug}`, {
    cache: 'no-store',
  });
  if (!response.ok) notFound();
  const posts = await response.json();
  const post = posts.find((p: Post) => p.slug === params.slug);

  if (!post) notFound();

  return (
    <div className="p-6 max-w-3xl mx-auto">
      <h1 className="text-4xl font-bold text-gray-800 mb-4">{post.title}</h1>
      <p className="text-gray-500 mb-6">
        Posted on {new Date(post.created_at).toLocaleDateString()}
      </p>
      <div className="prose prose-lg text-gray-700">
        {post.content.split('\n').map((paragraph, index) => (
          <p key={index}>{paragraph}</p>
        ))}
      </div>
      {/* Add comment section later */}
    </div>
  );
}