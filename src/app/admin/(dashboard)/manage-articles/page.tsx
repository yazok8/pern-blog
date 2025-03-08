import { prisma } from "@/lib/client";

export default async function Articles() {
    const articles = await prisma.article.findMany({
      where: { published: true },
      orderBy: { createdAt: 'desc' },
    });
  
    return (
      <div className="p-6 max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold text-gray-800 mb-6">My Tips</h1>
        {articles.length === 0 ? (
          <p className="text-gray-600">No tips yet—check back soon!</p>
        ) : (
          <div className="space-y-6">
            {articles.map((article) => (
              <div key={article.id} className="p-4 bg-white rounded-lg shadow-md">
                <h2 className="text-2xl font-semibold text-blue-600">{article.title}</h2>
                <p className="text-gray-600 mt-2">{article.excerpt || article.content.slice(0, 100) + '...'}</p>
                <a href={`/articles/${article.slug}`} className="text-blue-500 hover:underline mt-2 inline-block">
                  Read More
                </a>
              </div>
            ))}
          </div>
        )}
      </div>
    );
  }