import Container from '@/app/(client)/components/container';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { notFound } from 'next/navigation';
import { prisma } from 'prisma/client';


interface Article {
  id: string;
  title: string;
  slug: string;
  content: string;
  createdAt: Date;
}

export default async function ArticlePage({ params }: { params: { slug: string } }) {
  const article = await prisma.article.findFirst({
    where: { slug: params.slug, published: true },
  });

  if (!article) {
    notFound();
  }

  return (
    <Container>
    <Card className="p-6 max-w-3xl mx-auto">
      <CardHeader>
        <CardTitle  className="text-4xl font-bold text-gray-800 mb-4">{article.title}</CardTitle>
      </CardHeader>
      <CardContent>
      <p className="text-gray-500 mb-6">
        Published on {new Date(article.createdAt).toLocaleDateString()}
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