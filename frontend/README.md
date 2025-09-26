# Clean Next.js Boilerplate

A clean, scalable web application boilerplate built with modern frontend best practices.

## Features

- **Clean Architecture**: Well-organized folder structure with separation of concerns
- **TypeScript**: Strict typing throughout the application
- **Modular Components**: Reusable UI components with consistent styling
- **State Management**: Scalable approach using Convex for real-time data
- **Authentication**: Built-in user authentication with Convex Auth
- **Responsive Design**: Mobile-first, accessible design using Tailwind CSS
- **Error Handling**: Comprehensive error boundaries and loading states
- **SEO-Friendly**: Semantic HTML and proper metadata management
- **Developer Experience**: ESLint, Prettier, and TypeScript configurations

## Project Structure

```
src/
├── components/
│   ├── ui/              # Reusable UI components
│   ├── layout/          # Layout components
│   └── pages/           # Page components
├── hooks/               # Custom React hooks
├── utils/               # Utility functions
│   ├── constants.ts     # App constants
│   ├── formatters.ts    # Data formatting utilities
│   └── validation.ts    # Form validation utilities
└── lib/                 # External library configurations

convex/
├── schema.ts            # Database schema
├── users.ts             # User-related functions
└── auth.ts              # Authentication configuration
```

## Core Functionality

### Authentication
- Username/password login system
- Protected routes and components
- User session management

### Navigation
- Responsive navigation menu
- Mobile-friendly hamburger menu
- Active page highlighting

### Settings
- User preferences management
- Theme selection (light/dark/system)
- Notification preferences
- Language selection

### Dashboard
- User profile overview
- Settings summary
- Quick actions panel

## Getting Started

1. **Install dependencies**:
   ```bash
   npm install
   ```

2. **Start development server**:
   ```bash
   npm run dev
   ```

3. **Build for production**:
   ```bash
   npm run build
   ```

## Component Guidelines

### UI Components
- Located in `src/components/ui/`
- Follow consistent API patterns
- Include proper TypeScript interfaces
- Support common variants and sizes

### Layout Components
- Handle page structure and navigation
- Responsive by default
- Accessible navigation patterns

### Page Components
- Represent full page views
- Handle data fetching and error states
- Use layout components for structure

## Styling Guidelines

- **Tailwind CSS**: Utility-first CSS framework
- **Consistent Spacing**: Use predefined spacing scale
- **Color System**: Semantic color naming
- **Responsive Design**: Mobile-first approach
- **Accessibility**: WCAG 2.1 AA compliance

## State Management

- **Convex**: Real-time database and backend functions
- **Local State**: React hooks for component state
- **Persistent State**: localStorage for user preferences

## Error Handling

- **Error Boundaries**: Catch and display component errors
- **Loading States**: Consistent loading indicators
- **Form Validation**: Client-side validation with helpful messages
- **API Errors**: Graceful handling of network errors

## Performance

- **Code Splitting**: Automatic route-based splitting
- **Lazy Loading**: Components loaded on demand
- **Optimized Images**: Responsive image handling
- **Caching**: Efficient data caching with Convex

## Accessibility

- **Semantic HTML**: Proper HTML structure
- **ARIA Labels**: Screen reader support
- **Keyboard Navigation**: Full keyboard accessibility
- **Focus Management**: Visible focus indicators
- **Color Contrast**: WCAG AA compliant colors

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Contributing

1. Follow the existing code style
2. Add TypeScript types for new components
3. Include proper error handling
4. Test responsive design
5. Ensure accessibility compliance

## License

MIT License - see LICENSE file for details
