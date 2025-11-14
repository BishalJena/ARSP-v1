export function Footer() {
  return (
    <footer className="bg-white border-t mt-auto">
      <div className="container mx-auto px-4 py-6">
        <div className="flex flex-col md:flex-row justify-between items-center gap-4">
          <div className="text-sm text-gray-600">
            © {new Date().getFullYear()} ARSP. All rights reserved.
          </div>
          <div className="flex items-center gap-4 text-sm">
            <a
              href="/privacy"
              className="text-blue-600 hover:underline"
            >
              Privacy Policy
            </a>
            <span className="text-gray-400">·</span>
            <span className="text-gray-600">DPDP Compliant</span>
          </div>
        </div>
      </div>
    </footer>
  )
}
