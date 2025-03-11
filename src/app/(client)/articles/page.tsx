"use client";

import { useEffect, useState } from "react";
import { Loader } from "lucide-react";
import api from "@/lib/api";
import Container from "../components/container";

interface Article {
  id: string;
  title: string;
  slug: string;
  content: string;
  excerpt?: string | null;
  published: boolean;
}

interface PaginatedArticles {
  count: number;
  next: string | null;
  previous: string | null;
  results: Article[];
}

export default function Articles() {
  const [articles, setArticles] = useState<Article[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchArticles = async () => {
      try {
        // Use the axios instance:
        const response = await api.get<PaginatedArticles>("/articles");
        console.log('API response:', response.data);
        // Axios returns data in response.data
        setArticles(response.data.results);
      } catch (err) {
        setError((err as Error).message);
      } finally {
        setLoading(false);
      }
    };

    fetchArticles();
  }, []);

  if (loading) {
    return (
      <Container className="max-w-4xl">
        <Loader className="animate-spin" />
      </Container>
    );
  }

  if (error) {
    return (
      <Container>
        <p className="text-red-600">Error: {error}</p>
      </Container>
    );
  }

  return (
    <Container className="p-6 max-w-7xl mx-auto">
      <h1 className="text-4xl font-bold text-gray-800 mb-6">My Tips</h1>
      {articles.length === 0 ? (
        <p>No articles found.</p>
      ) : (
        <div className="flex flex-wrap gap-2 justify-start">
          {articles.map((article) => (
            <div key={article.id} className="p-4 bg-white rounded-lg shadow-md max-w-sm">
              <h2 className="text-2xl font-semibold text-blue-600">
                {article.title}
              </h2>
              <p className="text-gray-600 mt-2">
                {article.excerpt || article.content.slice(0, 100) + "..."}
              </p>
              <a
                href={`/articles/${article.slug}`}
                className="text-blue-500 hover:underline mt-2 inline-block"
              >
                Read More
              </a>
            </div>
          ))}
        </div>
      )}
    </Container>
  );
}
