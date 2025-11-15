class PDFPage:
    def __init__(self, reference: str, content: str):
        self.reference = reference
        self.content = content

class ComplianceParameter:
    def __init__(self, name: str, value: float, threshold: float):
        self.name = name
        self.value = value
        self.threshold = threshold

    def is_compliant(self) -> bool:
        return self.value <= self.threshold

class NonComplianceIssue:
    def __init__(self, parameter: ComplianceParameter):
        self.parameter = parameter
        self.message = f"Non-compliance detected for {self.parameter.name}: {self.parameter.value} exceeds threshold of {self.parameter.threshold}"