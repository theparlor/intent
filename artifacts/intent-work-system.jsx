import React, { useState } from 'react';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import {
  ArrowRight,
  Layers,
  Clock,
  Settings,
  BarChart3,
  CheckCircle2,
  AlertCircle,
  Zap,
} from 'lucide-react';

const IntentWorkSystem = () => {
  const [expandedCard, setExpandedCard] = useState(null);

  // Work Ontology Data
  const workUnits = [
    {
      id: 'signal',
      label: 'Signal',
      icon: Zap,
      description: 'Raw observation or request',
      details:
        'Unstructured input captured from design sessions, user feedback, or monitoring. The notice layer feeds these into the system.',
      color: 'from-yellow-50 to-orange-50',
      borderColor: 'border-yellow-300',
    },
    {
      id: 'intent',
      label: 'Intent',
      icon: AlertCircle,
      description: 'Declarative goal or outcome',
      details:
        'What we want to achieve. Parsed from signals, structured as goals. Orthogonal to time and implementation path.',
      color: 'from-orange-50 to-red-50',
      borderColor: 'border-orange-300',
    },
    {
      id: 'spec',
      label: 'Spec',
      icon: Settings,
      description: 'Detailed requirements & constraints',
      details:
        'How to achieve the intent. Includes business logic, edge cases, acceptance criteria. Agents consume specs as program input.',
      color: 'from-red-50 to-pink-50',
      borderColor: 'border-red-300',
    },
    {
      id: 'contract',
      label: 'Contract',
      icon: CheckCircle2,
      description: 'Interface & guarantees',
      details:
        'The boundary between components. Defines input types, output types, error handling. Enables parallelization.',
      color: 'from-pink-50 to-purple-50',
      borderColor: 'border-pink-300',
    },
    {
      id: 'capability',
      label: 'Capability',
      icon: Layers,
      description: 'Atomic skill or subsystem',
      details:
        'A unit of functionality that fulfills a contract. Can be built by agent, human, or hybrid. Tested independently.',
      color: 'from-purple-50 to-blue-50',
      borderColor: 'border-purple-300',
    },
    {
      id: 'feature',
      label: 'Feature',
      icon: BarChart3,
      description: 'Composed capability for users',
      details:
        'One or more capabilities composed into user-visible behavior. Has acceptance tests, telemetry, observability.',
      color: 'from-blue-50 to-cyan-50',
      borderColor: 'border-blue-300',
    },
    {
      id: 'product',
      label: 'Product',
      icon: ArrowRight,
      description: 'Integrated system for market',
      details:
        'A collection of features integrated into a coherent offering. Has versioning, release notes, user support.',
      color: 'from-cyan-50 to-green-50',
      borderColor: 'border-cyan-300',
    },
  ];

  // Three Dimensions Data
  const dimensions = [
    {
      title: 'Right Things (Discovery)',
      icon: AlertCircle,
      description: 'What should we build?',
      layers: [
        {
          name: 'Input: Signals',
          tools: ['Design sessions', 'User research', 'Monitoring', 'Customer feedback'],
        },
        {
          name: 'Parse: Intents',
          tools: ['Intent spec templates', 'Goal parsing', 'Constraint extraction'],
        },
        {
          name: 'Output: Prioritized roadmap',
          tools: ['Prioritization', 'Portfolio view', 'Impact estimation'],
        },
      ],
      color: 'bg-yellow-50',
    },
    {
      title: 'Right Time (Parallelization)',
      icon: Clock,
      description: 'When can we build it in parallel?',
      layers: [
        {
          name: 'Input: Specs',
          tools: ['Dependency graph', 'Contract analysis', 'Interface extraction'],
        },
        {
          name: 'Schedule: Critical path',
          tools: ['DAG solver', 'Work partitioning', 'Resource leveling'],
        },
        {
          name: 'Output: Work streams',
          tools: ['Sprint planning', 'Team allocation', 'Milestone tracking'],
        },
      ],
      color: 'bg-blue-50',
    },
    {
      title: 'Right Way (Governance)',
      icon: Settings,
      description: 'How do we build it correctly?',
      layers: [
        {
          name: 'Input: Contracts',
          tools: ['Interface specs', 'SLA definitions', 'Architecture rules'],
        },
        {
          name: 'Enforce: Quality gates',
          tools: ['Design review', 'Code review', 'Test coverage', 'Performance budgets'],
        },
        {
          name: 'Output: Capability',
          tools: ['Integration', 'Release', 'Documentation', 'Monitoring'],
        },
      ],
      color: 'bg-purple-50',
    },
  ];

  // Agent Flow Data
  const agentFlow = [
    {
      phase: 'Notice',
      description: 'Capture signals from design sessions, user feedback, monitoring',
      agent: 'Observation Agent',
      duration: 'Continuous',
    },
    {
      phase: 'Parse',
      description: 'Extract intents and specs from signals',
      agent: 'Intent Parser',
      duration: '< 1 minute',
    },
    {
      phase: 'Plan',
      description: 'Analyze parallelization opportunities and schedule work',
      agent: 'Scheduler',
      duration: '< 5 minutes',
    },
    {
      phase: 'Build',
      description: 'Execute contracts and compose capabilities',
      agent: 'Developer Agents',
      duration: '< 2 hours',
    },
    {
      phase: 'Test',
      description: 'Validate contracts and acceptance criteria',
      agent: 'Test Agent',
      duration: '< 10 minutes',
    },
    {
      phase: 'Observe',
      description: 'Gather telemetry and feedback for next cycle',
      agent: 'Monitor Agent',
      duration: 'Continuous',
    },
  ];

  // Dashboard Data
  const dashboardMetrics = [
    { label: 'Active Intents', value: 12, trend: '+3 this week' },
    { label: 'Specs in Flight', value: 8, trend: '+2 in progress' },
    { label: 'Capabilities Built', value: 24, trend: '+4 completed' },
    { label: 'Feature Velocity', value: '2.4 features/sprint', trend: '+15% vs last sprint' },
  ];

  // Agile vs Intent Comparison
  const comparison = [
    {
      agile: 'User Story',
      intent: 'Signal → Intent',
      rationale: 'Stories are for humans; Signals and Intents are declarative machine-consumable goals',
    },
    {
      agile: 'Acceptance Criteria',
      intent: 'Spec',
      rationale: 'Spec is the primary unit; AC is implicit in contract + tests',
    },
    {
      agile: 'Sprint Planning',
      intent: 'Schedule (DAG-based)',
      rationale: 'Fixed sprints create artificial batching; DAG scheduling discovers optimal parallelization',
    },
    {
      agile: 'Story Points',
      intent: 'Capability atoms',
      rationale: 'Story points are estimates; Capabilities are actual deployable units',
    },
    {
      agile: 'Backlog Grooming',
      intent: 'Intent Refinement',
      rationale: 'Grooming assumes humans decide priority; Intent system separates discovery from scheduling',
    },
    {
      agile: 'Sprint Retrospective',
      intent: 'Observe Cycle',
      rationale: 'Retros are periodic; Observe is continuous, feeding signals back into the system',
    },
    {
      agile: 'Burndown Chart',
      intent: 'Capability Health Dashboard',
      rationale: 'Burndown measures human output; Health tracks machine-testable state changes',
    },
    {
      agile: 'Release Notes',
      intent: 'Feature Trace',
      rationale: 'Notes describe features; Trace links features back to original signals',
    },
    {
      agile: 'Product Owner',
      intent: 'Intent Parser + Router',
      rationale: 'PO prioritizes; Intent system automates discovery and routing',
    },
  ];

  const OntologyTab = () => (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {workUnits.map((unit) => {
          const IconComponent = unit.icon;
          const isExpanded = expandedCard === unit.id;
          return (
            <div
              key={unit.id}
              onClick={() => setExpandedCard(isExpanded ? null : unit.id)}
              className={`relative cursor-pointer transition-all duration-300 ${
                isExpanded ? 'md:col-span-2 lg:col-span-3 xl:col-span-4' : ''
              }`}
            >
              <Card
                className={`h-full border-2 ${unit.borderColor} bg-gradient-to-br ${unit.color} hover:shadow-lg transition-shadow`}
              >
                <CardHeader className="pb-3">
                  <div className="flex items-center gap-2">
                    <IconComponent className="w-5 h-5" />
                    <CardTitle className="text-lg">{unit.label}</CardTitle>
                  </div>
                  <CardDescription>{unit.description}</CardDescription>
                </CardHeader>
                {isExpanded && (
                  <CardContent>
                    <p className="text-sm text-gray-700">{unit.details}</p>
                  </CardContent>
                )}
              </Card>
            </div>
          );
        })}
      </div>
    </div>
  );

  const DimensionsTab = () => (
    <div className="space-y-6">
      {dimensions.map((dim, idx) => {
        const IconComponent = dim.icon;
        return (
          <div key={idx} className={`p-6 rounded-lg border-2 border-gray-200 ${dim.color}`}>
            <div className="flex items-center gap-3 mb-4">
              <IconComponent className="w-6 h-6" />
              <div>
                <h3 className="text-xl font-semibold">{dim.title}</h3>
                <p className="text-sm text-gray-600">{dim.description}</p>
              </div>
            </div>
            <div className="space-y-3">
              {dim.layers.map((layer, layerIdx) => (
                <div key={layerIdx} className="bg-white rounded-lg p-4 border border-gray-200">
                  <h4 className="font-semibold text-sm mb-2">{layer.name}</h4>
                  <div className="flex flex-wrap gap-2">
                    {layer.tools.map((tool, toolIdx) => (
                      <span
                        key={toolIdx}
                        className="inline-block bg-gray-100 px-2 py-1 rounded text-xs"
                      >
                        {tool}
                      </span>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
        );
      })}
    </div>
  );

  const AgentFlowTab = () => (
    <div className="space-y-4">
      {agentFlow.map((flow, idx) => (
        <div key={idx} className="flex items-start gap-4">
          <div className="flex-1 bg-blue-50 rounded-lg p-4 border border-blue-200">
            <div className="flex items-center gap-2 mb-2">
              <span className="inline-flex items-center justify-center w-8 h-8 rounded-full bg-blue-500 text-white font-semibold text-sm">
                {idx + 1}
              </span>
              <h4 className="text-lg font-semibold">{flow.phase}</h4>
            </div>
            <p className="text-sm text-gray-700 mb-2">{flow.description}</p>
            <div className="flex justify-between text-xs text-gray-600">
              <span className="font-semibold">Agent: {flow.agent}</span>
              <span>Duration: {flow.duration}</span>
            </div>
          </div>
          {idx < agentFlow.length - 1 && (
            <div className="flex items-center justify-center h-full">
              <ArrowRight className="w-5 h-5 text-gray-400" />
            </div>
          )}
        </div>
      ))}
    </div>
  );

  const DashboardTab = () => (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      {dashboardMetrics.map((metric, idx) => (
        <Card key={idx} className="border-2 border-purple-200 bg-purple-50">
          <CardHeader>
            <CardTitle className="text-lg">{metric.label}</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-4xl font-bold text-purple-600 mb-2">{metric.value}</div>
            <p className="text-sm text-gray-600">{metric.trend}</p>
          </CardContent>
        </Card>
      ))}
    </div>
  );

  const VersusTab = () => (
    <div className="space-y-4">
      <div className="grid grid-cols-3 gap-4 mb-4">
        <div className="font-semibold text-center p-3 bg-blue-100 rounded">Agile Concept</div>
        <div className="font-semibold text-center p-3 bg-green-100 rounded">Intent Equivalent</div>
        <div className="font-semibold text-center p-3 bg-gray-100 rounded">Why the Shift</div>
      </div>
      {comparison.map((row, idx) => (
        <div key={idx} className="grid grid-cols-3 gap-4 items-start">
          <div className="p-3 bg-blue-50 rounded border border-blue-200 text-sm">
            {row.agile}
          </div>
          <div className="p-3 bg-green-50 rounded border border-green-200 text-sm font-semibold">
            {row.intent}
          </div>
          <div className="p-3 bg-gray-50 rounded border border-gray-200 text-sm">
            {row.rationale}
          </div>
        </div>
      ))}
    </div>
  );

  return (
    <div className="w-full max-w-7xl mx-auto p-6 bg-white">
      <div className="mb-8">
        <h1 className="text-4xl font-bold mb-2">Intent Work System</h1>
        <p className="text-gray-600">
          An agent-native alternative to Agile. Replaces tickets and sprints with declarative work units and
          continuous parallelization.
        </p>
      </div>

      <Tabs defaultValue="ontology" className="w-full">
        <TabsList className="grid w-full grid-cols-5">
          <TabsTrigger value="ontology">Work Ontology</TabsTrigger>
          <TabsTrigger value="dimensions">Three Dimensions</TabsTrigger>
          <TabsTrigger value="flow">Agent Flow</TabsTrigger>
          <TabsTrigger value="dashboard">Dashboard</TabsTrigger>
          <TabsTrigger value="versus">Agile → Intent</TabsTrigger>
        </TabsList>

        <TabsContent value="ontology" className="mt-6">
          <OntologyTab />
        </TabsContent>

        <TabsContent value="dimensions" className="mt-6">
          <DimensionsTab />
        </TabsContent>

        <TabsContent value="flow" className="mt-6">
          <AgentFlowTab />
        </TabsContent>

        <TabsContent value="dashboard" className="mt-6">
          <DashboardTab />
        </TabsContent>

        <TabsContent value="versus" className="mt-6">
          <VersusTab />
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default IntentWorkSystem;