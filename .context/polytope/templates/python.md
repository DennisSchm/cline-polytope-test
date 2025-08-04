# Directives for Creating A Python Component

## CRITICAL: Always generate and customize components, never just create setup scripts!

When asked to create a Python component as part of a larger task:
1. **ALWAYS** run the scaffold command to generate the component if an appropiate template is available
2. **ALWAYS** add required packages using the component's add module
3. **ALWAYS** customize the generated code to meet the specific requirements
4. **NEVER** just create a setup script and leave component generation to the user

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

**IMPORTANT**: The add module is only available AFTER the component has been generated and the main polytope.yml includes the component's polytope.yml file.

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

## After generating components
1. Update the main polytope.yml to include the generated component's polytope.yml file using the `include` directive
2. Customize the generated code files to implement the specific functionality required
3. Update configuration files as needed

## Specific packages to use
For api servers, use fastapi with uvicorn.
