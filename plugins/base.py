"""
Base classes for source-format adapter plugins.

Plugins convert one raw input item into one canonical entity dict containing
$schema. They do not receive validation context and do not run validation rules.
"""

from abc import ABC, abstractmethod


class PluginError(Exception):
    """Raised when source data cannot be converted into a canonical entity."""


class ValidationPlugin(ABC):
    """Base class for one-item source-format adapters."""

    @abstractmethod
    def convert(self, input_data):
        """Convert one raw input item into one canonical entity dict containing $schema."""
