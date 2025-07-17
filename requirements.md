# Profile Requirements

Essential information about profile dependencies and requirements.

## Python Dependencies

Profiles should only include **external dependencies** not managed by ComfyUI or extensions.

### ✅ Include These
- External packages required by extensions (e.g., `insightface` for IPAdapter)
- Custom Python packages for specialized functionality
- Version-specific dependencies for reproducibility

### ❌ Don't Include These
- Core ComfyUI dependencies
- Dependencies managed by ComfyUI extensions
- System packages (handled by Docker base image)

## Example Requirements

```txt
# External dependencies for IPAdapter extension
insightface>=0.7.3

# Custom package for specialized functionality
my-custom-package==1.0.0
```

## Best Practices

1. **Minimal Dependencies**: Only include what's absolutely necessary
2. **Version Pinning**: Use specific versions for reproducibility
3. **Documentation**: Explain why each dependency is needed
4. **Testing**: Verify dependencies work in the container environment

## Validation

The Profile Manager automatically validates requirements:
- Checks for circular dependencies
- Verifies package compatibility
- Ensures no conflicts with core dependencies