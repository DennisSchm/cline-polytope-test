# Directives for Creating a React App with Polytope

## Creating the component
**CRITICAL**: ALWAYS make sure that the template argument points inside the `.templates/` directory!

Use the build-in `polytope/scaffold` module to create a starting project via:
`pt run --non-interactive "polytope/scaffold{template: '.templates/frontend', path: 'my-component-name'}"`

**Parameter explanation:**
- `template`: Points to the path where the template is stored (e.g., `.templates/frontend`)
- `path`: Points to the directory where the new project will be created

### Examples:
- Frontend component: `pt run --non-interactive "polytope/scaffold{template: '.templates/frontend', path: 'frontend'}"`
- Another frontend: `pt run --non-interactive "polytope/scaffold{template: '.templates/frontend', path: 'web-app'}"`

## Adding packages to React components
Each React component created with the template includes a custom `{component-name}-add` module for adding packages.

**Usage:**
```bash
pt run --non-interactive "{component-name}-add{packages: 'package-name'}"
```

**Examples:**
- For a 'frontend' component: `pt run --non-interactive "frontend-add{packages: 'axios'}"`
- For a 'web-app' component: `pt run --non-interactive "web-app-add{packages: 'react-query'}"`
- Multiple packages: `pt run --non-interactive "frontend-add{packages: 'axios react-query'}"`

**IMPORTANT:** 
- Do NOT specify package versions unless specifically requested by the user
- Use space-separated package names for multiple packages
- The packages parameter accepts comma or whitespace-separated lists

## Dependencies
This creates a project based on bun and React with React Router v7.
