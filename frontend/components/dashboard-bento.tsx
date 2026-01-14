"use client"

import { BentoGrid, BentoGridItem } from "./bento-grid"
import { Area, AreaChart, Bar, BarChart, CartesianGrid, Line, LineChart, XAxis, YAxis } from "recharts"
import { ChartConfig, ChartContainer, ChartTooltip, ChartTooltipContent, COLORS } from "@/components/charts"

// Sample data
const lineData = [
  { month: "Jan", value: 186 },
  { month: "Feb", value: 305 },
  { month: "Mar", value: 237 },
  { month: "Apr", value: 273 },
  { month: "May", value: 209 },
  { month: "Jun", value: 314 },
]

const barData = [
  { name: "Agent A", value: 400 },
  { name: "Agent B", value: 300 },
  { name: "Agent C", value: 200 },
  { name: "Agent D", value: 278 },
]

const areaData = [
  { month: "Jan", desktop: 186, mobile: 80 },
  { month: "Feb", desktop: 305, mobile: 200 },
  { month: "Mar", desktop: 237, mobile: 120 },
  { month: "Apr", desktop: 273, mobile: 190 },
  { month: "May", desktop: 209, mobile: 130 },
  { month: "Jun", desktop: 214, mobile: 140 },
]

const chartConfig = {
  value: {
    label: "Value",
    color: COLORS[0],
  },
  desktop: {
    label: "Desktop",
    color: COLORS[0],
  },
  mobile: {
    label: "Mobile",
    color: COLORS[2],
  },
} satisfies ChartConfig

export function DashboardBento() {
  return (
    <div className="container mx-auto py-8">
      <h1 className="mb-8 text-3xl font-bold text-white">Analytics Dashboard</h1>
      
      <BentoGrid>
        {/* Large chart - spans 2 columns */}
        <BentoGridItem colSpan={2} rowSpan={2}>
          <div className="flex h-full flex-col">
            <h3 className="mb-2 text-xl font-semibold text-white">Monthly Trends</h3>
            <p className="mb-4 text-sm text-gray-400">
              Performance over the last 6 months
            </p>
            <ChartContainer config={chartConfig} className="h-full w-full">
              <AreaChart data={areaData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis 
                  dataKey="month" 
                  stroke="#94a3b8"
                  style={{ fontSize: '12px' }}
                />
                <YAxis 
                  stroke="#94a3b8"
                  style={{ fontSize: '12px' }}
                />
                <ChartTooltip content={<ChartTooltipContent />} />
                <Area
                  type="monotone"
                  dataKey="desktop"
                  stackId="1"
                  stroke={COLORS[0]}
                  fill={COLORS[0]}
                  fillOpacity={0.6}
                />
                <Area
                  type="monotone"
                  dataKey="mobile"
                  stackId="1"
                  stroke={COLORS[2]}
                  fill={COLORS[2]}
                  fillOpacity={0.6}
                />
              </AreaChart>
            </ChartContainer>
          </div>
        </BentoGridItem>

        {/* Stat card */}
        <BentoGridItem>
          <div className="flex h-full flex-col justify-between">
            <div>
              <p className="text-sm text-gray-400">Total Users</p>
              <h2 className="mt-2 text-4xl font-bold text-white">12,345</h2>
            </div>
            <div className="mt-4">
              <span className="text-sm text-[#5ca3d8]">↑ 12.5%</span>
              <span className="ml-2 text-sm text-gray-400">from last month</span>
            </div>
          </div>
        </BentoGridItem>

        {/* Bar chart */}
        <BentoGridItem>
          <div className="flex h-full flex-col">
            <h3 className="mb-2 text-lg font-semibold text-white">Agent Performance</h3>
            <ChartContainer config={chartConfig} className="h-full w-full">
              <BarChart data={barData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis 
                  dataKey="name" 
                  stroke="#94a3b8"
                  style={{ fontSize: '12px' }}
                />
                <YAxis 
                  stroke="#94a3b8"
                  style={{ fontSize: '12px' }}
                />
                <ChartTooltip content={<ChartTooltipContent />} />
                <Bar dataKey="value" fill={COLORS[0]} radius={[4, 4, 0, 0]} />
              </BarChart>
            </ChartContainer>
          </div>
        </BentoGridItem>

        {/* Line chart - spans 2 columns */}
        <BentoGridItem colSpan={2}>
          <div className="flex h-full flex-col">
            <h3 className="mb-2 text-lg font-semibold text-white">Growth Rate</h3>
            <p className="mb-4 text-sm text-gray-400">Monthly progression</p>
            <ChartContainer config={chartConfig} className="h-full w-full">
              <LineChart data={lineData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis 
                  dataKey="month" 
                  stroke="#94a3b8"
                  style={{ fontSize: '12px' }}
                />
                <YAxis 
                  stroke="#94a3b8"
                  style={{ fontSize: '12px' }}
                />
                <ChartTooltip content={<ChartTooltipContent />} />
                <Line
                  type="monotone"
                  dataKey="value"
                  stroke={COLORS[0]}
                  strokeWidth={2}
                  dot={{ fill: COLORS[0], r: 4 }}
                  activeDot={{ r: 6, fill: COLORS[2] }}
                />
              </LineChart>
            </ChartContainer>
          </div>
        </BentoGridItem>

        {/* Another stat card */}
        <BentoGridItem>
          <div className="flex h-full flex-col justify-between">
            <div>
              <p className="text-sm text-gray-400">Revenue</p>
              <h2 className="mt-2 text-4xl font-bold text-white">$45.2K</h2>
            </div>
            <div className="mt-4">
              <span className="text-sm text-[#5ca3d8]">↑ 8.1%</span>
              <span className="ml-2 text-sm text-gray-400">vs last quarter</span>
            </div>
          </div>
        </BentoGridItem>

        {/* Full width chart */}
        <BentoGridItem colSpan={3}>
          <div className="flex h-full flex-col">
            <h3 className="mb-2 text-xl font-semibold text-white">Detailed Analytics</h3>
            <p className="mb-4 text-sm text-gray-400">
              Comprehensive view across all metrics
            </p>
            <ChartContainer config={chartConfig} className="h-full w-full">
              <LineChart data={lineData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis 
                  dataKey="month" 
                  stroke="#94a3b8"
                  style={{ fontSize: '12px' }}
                />
                <YAxis 
                  stroke="#94a3b8"
                  style={{ fontSize: '12px' }}
                />
                <ChartTooltip content={<ChartTooltipContent />} />
                <Line
                  type="monotone"
                  dataKey="value"
                  stroke={COLORS[0]}
                  strokeWidth={3}
                  dot={false}
                />
              </LineChart>
            </ChartContainer>
          </div>
        </BentoGridItem>
      </BentoGrid>
    </div>
  )
}