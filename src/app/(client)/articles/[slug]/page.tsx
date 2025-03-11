// app/articles/[slug]/page.tsx
import Container from '@/app/(client)/components/container';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { notFound } from 'next/navigation';

interface Article {
  id: number;
  title: string;
  slug: string;
  content: string;
  excerpt?: string | null;
  published: boolean;
  created_at: string; // Django typically uses snake_case
}

export default async function ArticlePage(props: { params: { slug: string } }) {
  // Await the params to satisfy Next.js's requirement
  const params = await Promise.resolve(props.params);
  const { slug } = params; // Now it's "awaited"
  
  // 1. Fetch from Django
  const res = await fetch(`http://localhost:8000/api/articles/${slug}/`, {
    cache: 'no-store',
  });

  if (!res.ok) {
    notFound();
  }

  const article: Article = await res.json();

  if (!article.published) {
    notFound();
  }

  return (
    <Container>
      <Card className="p-6 max-w-3xl mx-auto">
        <CardHeader>
          <CardTitle className="text-4xl font-bold text-gray-800 mb-4">
            {article.title}
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-gray-500 mb-6">
            Published on {new Date(article.created_at).toLocaleDateString()}
          </p>
          <div className="prose prose-lg text-gray-700">
            {article.content.split('\n').map((paragraph, index) => (
              <p key={index}>{paragraph}</p>
            ))}
          </div>
        </CardContent>
      </Card>
    </Container>
  );
}

