import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import toast from 'react-hot-toast';
import { useAuthStore } from '../store/auth';

interface LoginForm {
  email: string;
  password: string;
}

export default function LoginPage() {
  const navigate = useNavigate();
  const login = useAuthStore((state) => state.login);
  const [isLoading, setIsLoading] = useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginForm>();

  const onSubmit = async (data: LoginForm) => {
    setIsLoading(true);
    try {
      await login(data.email, data.password);
      toast.success('Authenticated');
      navigate('/');
    } catch {
      toast.error('Invalid credentials');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex bg-white">
      {/* Left side - Info panel */}
      <div className="hidden lg:flex lg:w-1/2 bg-black text-white">
        <div className="flex flex-col justify-between p-12 w-full">
          <div>
            <div className="font-mono text-sm tracking-tight">
              <span className="text-white">RWA</span>
              <span className="text-gray-500 ml-2">v2.0</span>
            </div>
          </div>
          
          <div className="space-y-12">
            <div>
              <h1 className="text-4xl font-semibold tracking-tight mb-4">
                Rural Water Association
              </h1>
              <p className="text-gray-400 text-lg max-w-md">
                Digital transformation platform for water utility management
              </p>
            </div>
            
            <div className="space-y-6 font-mono text-sm">
              <div className="flex items-start gap-4">
                <span className="text-gray-500 w-6">01</span>
                <div>
                  <div className="text-white">NRW MANAGEMENT</div>
                  <div className="text-gray-500">IWA methodology water balance</div>
                </div>
              </div>
              <div className="flex items-start gap-4">
                <span className="text-gray-500 w-6">02</span>
                <div>
                  <div className="text-white">ENERGY OPTIMIZATION</div>
                  <div className="text-gray-500">Pump scheduling 15-30% savings</div>
                </div>
              </div>
              <div className="flex items-start gap-4">
                <span className="text-gray-500 w-6">03</span>
                <div>
                  <div className="text-white">COMPLIANCE TRACKING</div>
                  <div className="text-gray-500">EPA SDWA obligations & reporting</div>
                </div>
              </div>
            </div>
          </div>

          <div className="text-xs text-gray-600 font-mono">
            © 2025 VISIONBLOX LLC
          </div>
        </div>
      </div>

      {/* Right side - Login form */}
      <div className="flex-1 flex items-center justify-center p-8">
        <div className="w-full max-w-sm">
          <div className="lg:hidden mb-12">
            <div className="font-mono text-sm tracking-tight">
              <span className="text-black">RWA</span>
              <span className="text-gray-400 ml-2">v2.0</span>
            </div>
          </div>

          <div className="mb-8">
            <h2 className="text-2xl font-semibold text-black tracking-tight">Sign in</h2>
            <p className="text-gray-500 mt-1 text-sm">Access your dashboard</p>
          </div>

          <form onSubmit={handleSubmit(onSubmit)} className="space-y-5">
            <div>
              <label
                htmlFor="email"
                className="block text-xs uppercase tracking-wider text-gray-500 mb-2"
              >
                Email
              </label>
              <input
                {...register('email', {
                  required: 'Email is required',
                  pattern: {
                    value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                    message: 'Invalid email address',
                  },
                })}
                type="email"
                className="input"
                placeholder="operator@example.com"
              />
              {errors.email && (
                <p className="mt-1.5 text-xs text-red-600">{errors.email.message}</p>
              )}
            </div>

            <div>
              <label
                htmlFor="password"
                className="block text-xs uppercase tracking-wider text-gray-500 mb-2"
              >
                Password
              </label>
              <input
                {...register('password', {
                  required: 'Password is required',
                  minLength: {
                    value: 6,
                    message: 'Password must be at least 6 characters',
                  },
                })}
                type="password"
                className="input"
                placeholder="••••••••"
              />
              {errors.password && (
                <p className="mt-1.5 text-xs text-red-600">{errors.password.message}</p>
              )}
            </div>

            <button
              type="submit"
              disabled={isLoading}
              className="btn btn-primary w-full mt-2"
            >
              {isLoading ? 'AUTHENTICATING...' : 'SIGN IN'}
            </button>
          </form>

          <div className="mt-8 p-4 border border-gray-200">
            <p className="text-xs text-gray-500 font-mono text-center">
              DEMO: any email / any password (6+ chars)
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
