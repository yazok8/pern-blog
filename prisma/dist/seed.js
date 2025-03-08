import { prisma } from '../client.js';
import { ObjectId } from 'mongodb';

async function main() {
  console.log('Starting seed process...');
  
  // Clean existing data
  console.log('Cleaning existing data...');
  await prisma.article.deleteMany();
  
  // Create a temporary user or find an existing one
  console.log('Creating/finding a user...');
  let user = await prisma.user.findFirst();
  
  if (!user) {
    user = await prisma.user.create({
      data: {
        name: 'Seed User',
        email: 'seed@example.com',
        password: 'password123', // In production, you'd hash this
        role: 'AUTHOR'
      }
    });
    console.log('Created new user:', user.id);
  } else {
    console.log('Using existing user:', user.id);
  }
  
  // Create article with the valid user ID
  console.log('Creating article...');
  await prisma.article.create({
    data: {
      title: '3 Supplements That Helped Me',
      slug: '3-supplements-that-helped-me',
      content: '1. Magnesium - Calmed my nerves after tough days...\n2. Vitamin D - Boosted my mood in Canada&apos;s winters...\n3. Omega-3 - enhanced my focus and improved my depresson... ',
      excerpt: 'Simple supplements that eased my chronic pain.',
      published: true,
      authorId: user.id,
      categoryIds: [],
      tagIds: [],
    },
  });
  
  console.log('Seeded article successfully!');
}

main()
  .then(async () => {
    console.log('Seeding completed successfully');
    await prisma.$disconnect();
  })
  .catch(async (e) => {
    console.error('Error during seeding:', e);
    await prisma.$disconnect();
    process.exit(1);
  });