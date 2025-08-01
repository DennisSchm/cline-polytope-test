import type { Route } from "./+types/home";
import { Welcome } from "../welcome/welcome";

export function meta({}: Route.MetaArgs) {
  return [
    { title: "{{ project-name }}" },
    { name: "description", content: "Welcome to {{ project-name }}!" },
  ];
}

export default function Home() {
  return <div>hello</div>;
}
