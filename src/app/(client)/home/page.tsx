import Link from "next/link";
import Container from "../components/container";

export default function Homepage() {
    return (
      <Container className="max-w-6xl mx-auto">
        <h1 className="text-5xl font-bold text-blue-600">BreakLoose</h1>
        <p className="text-xl text-gray-700 mt-4 text-center">
          Guiding you through post-traumatic chronic pain with some healthy changes to your lifestyles, proven steps.
        </p>
        <div className="mt-7">
        <Link href="/articles" className="mt-6 px-6 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600">
          Read My Tips
        </Link>
        </div>
      </Container>
    );
  }