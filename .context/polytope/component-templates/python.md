# Directives for Creating A Python Component

## Creating the component
**CRITICAL**: ALWAYS make sure that the template argument points inside the `.templates/` directory!

Use the build-in `polytope/scaffold` module to create a starting project via:
`pt run --non-interactive "polytope/scaffold{template: '.templates/python-api', path: 'my-component-name'}"`

**Parameter explanation:**
- `template`: Points to the path where the template is stored (e.g., `.templates/python-api`)
- `path`: Points to the directory where the new project will be created

### Examples:
- API component: `pt run --non-interactive "polytope/scaffold{template: '.templates/python-api', path: 'api'}"`
- Another API: `pt run --non-interactive "polytope/scaffold{template: '.templates/python-api', path: 'backend'}"`

## Adding packages to Python components
Each Python component created with the template includes a custom `{component-name}-add` module for adding packages.

**Usage:**
```bash
pt run --non-interactive "{component-name}-add{packages: 'package-name'}"
```

**Examples:**
- For an 'api' component: `pt run --non-interactive "api-add{packages: 'kafka-python'}"`
- For a 'backend' component: `pt run --non-interactive "backend-add{packages: 'redis'}"`
- Multiple packages: `pt run --non-interactive "api-add{packages: 'kafka-python requests'}"`

**IMPORTANT:** 
- Do NOT specify package versions unless specifically requested by the user
- Use space-separated package names for multiple packages
- The packages parameter accepts comma or whitespace-separated lists

## Specific packages to use
For api servers, use fastapi with uvicorn.
