# Directives for Creating a React App with Polytope
Create a separate project directory for the frontend, even if it's the only project you are creating.

Generate scaffolding via `pt run --non-interactive "create-component{template: frontend, path: my-component-root-path}"`, and use `bun add` to install dependencies. DO NOT try to guess package versions! Let bun handle this for you!

This creates a project based on bun and React with React Router v7.