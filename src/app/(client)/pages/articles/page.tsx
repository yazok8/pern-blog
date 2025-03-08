"use client";

import { useEffect, useState } from "react";
import Container from "../../components/container";
import { Button } from "@/components/ui/button";
import { Loader } from "lucide-react";

interface Article {
    id: string;
    title: string;
    slug: string;
    content: string;
    excerpt?: string | null;
    published: boolean;
}

export default function Articles() {
  const [articles, setArticles] = useState<Article[]>([]);
    const [showTip, setShowTip] = useState(false);

    useEffect(() => {
      fetch('/api/articles')
        .then(res => res.json())
        .then(data => setArticles(data))
        .catch(err => console.error("Error fetching articles:", err));
    }, []);

    return (
      <Container className="p-6 max-w-4xl mx-auto">                                                                                                                       
        <h1 className="text-4xl font-bold text-gray-800 mb-6">My Tips</h1>
  {articles.length === 0 ? (
        <Loader className="animate-spin" />
      ) : (
        <div className="space-y-6">
          {articles.map((article) => (
            <div key={article.id} className="p-4 bg-white rounded-lg shadow-md">
              <h2 className="text-2xl font-semibold text-blue-600">{article.title}</h2>
              <p className="text-gray-600 mt-2">{article.excerpt || article.content.slice(0, 100) + '...'}</p>
              <a href={`/pages/articles/${article.slug}`} className="text-blue-500 hover:underline mt-2 inline-block">
                Read More
              </a>
            </div>
          ))}
        </div>
      )}
      </Container>
    );
  }