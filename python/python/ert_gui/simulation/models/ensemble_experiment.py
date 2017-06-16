from res.enkf.enums import HookRuntime
from ert_gui.simulation.models import BaseRunModel, ErtRunError

class EnsembleExperiment(BaseRunModel):

    def __init__(self):
        super(EnsembleExperiment, self).__init__("Ensemble Experiment")

    def runSimulations(self, job_queue,  arguments):
        self.setPhase(0, "Running simulations...", indeterminate=False)
        active_realization_mask = arguments["active_realizations"]

        active_realizations = 0;
        for b in active_realization_mask:
           if (b == 1):
              active_realizations = active_realizations + 1


        self.setPhaseName("Pre processing...", indeterminate=True)
        self.ert().getEnkfSimulationRunner().createRunPath(active_realization_mask, 0)
        self.ert().getEnkfSimulationRunner().runWorkflows( HookRuntime.PRE_SIMULATION )

        self.setPhaseName("Running ensemble experiment...", indeterminate=False)

        num_successful_realizations = self.ert().getEnkfSimulationRunner().runEnsembleExperiment(job_queue, active_realization_mask)

        self.assertHaveSufficientRealizations(num_successful_realizations, active_realizations)

        self.setPhaseName("Post processing...", indeterminate=True)
        self.ert().getEnkfSimulationRunner().runWorkflows( HookRuntime.POST_SIMULATION )

        self.setPhase(1, "Simulations completed.") # done...



