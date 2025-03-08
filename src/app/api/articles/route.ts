import { NextResponse } from 'next/server';
import { prisma } from 'prisma/client';


export async function GET() {
  const articles = await prisma.article.findMany({
    where: { published: true },
    orderBy: { createdAt: 'desc' },
  });
  return NextResponse.json(articles);
}