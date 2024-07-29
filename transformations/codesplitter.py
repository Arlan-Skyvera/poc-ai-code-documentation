from typing import Any, List, Sequence

from llama_index.core.schema import (
    BaseNode,
    TransformComponent
)
from llama_index.core.node_parser import (
    CodeSplitter,
    SentenceSplitter,
    TextSplitter
)
from llama_index.core.bridge.pydantic import Field, PrivateAttr

from tree_sitter_languages import get_parser

from utils.pl import load_mapping

DEFAULT_CHUNK_LINES = 40
DEFAULT_LINES_OVERLAP = 15
DEFAULT_MAX_CHARS = 1500

class DynamicCodeSplitter(TextSplitter):
    """
    Code Splitter is implemented as a singleton
    One instance handles multiple documents
    Task:
     - Must override split_text method to handle dynamic parser
    """
    chunk_lines: int = Field(
        default=DEFAULT_CHUNK_LINES,
        description="The number of lines to include in each chunk.",
        gt=0,
    )
    chunk_lines_overlap: int = Field(
        default=DEFAULT_LINES_OVERLAP,
        description="How many lines of code each chunk overlaps with.",
        gt=0,
    )
    max_chars: int = Field(
        default=DEFAULT_MAX_CHARS,
        description="Maximum number of characters per chunk.",
        gt=0,
    )
    _mapping = PrivateAttr()
    _sentence_splitter = PrivateAttr()
    _code_splitter = PrivateAttr()

    def __init__(
        self, 
        chunk_lines: int = DEFAULT_CHUNK_LINES,
        chunk_lines_overlap: int = DEFAULT_LINES_OVERLAP,
        max_chars: int = DEFAULT_MAX_CHARS,
        *args,
        **kwargs
    ):
        self._mapping = load_mapping()

        self._code_splitter = CodeSplitter(language='java', **kwargs)
        self._sentence_splitter = SentenceSplitter(**kwargs)

        super().__init__(
            chunk_lines=chunk_lines,
            chunk_lines_overlap=chunk_lines_overlap,
            max_chars=max_chars,
        )
    
    def _parse_nodes(self, nodes: Sequence[BaseNode], show_progress: bool = False, **kwargs: Any) -> List[BaseNode]:
        """
        This method contains the node metadata info that contains the file extension
        Requirements:
         - (Assume first) Prove that it is enough to have the first node metadata info for it will be consistent with all other nodes since they belong to the same document
        """
        repr_node = nodes[0]

        file_name = repr_node.metadata.get('file_name')
        file_extension = '.' + str(file_name).split('.')[-1]
        
        language = self._mapping.get(file_extension)

        if (
            language is None
        ) or (
            language and language['type'] != 'programming'
        ):
            # Defaults to sentence splitter
            return self._sentence_splitter._parse_nodes(nodes, show_progress, **kwargs)

        self._parser = get_parser(language)
        
        return self._code_splitter._parse_nodes(nodes, show_progress, **kwargs)

    def split_text(self, text: str) -> List[str]:
        raise NotImplementedError()