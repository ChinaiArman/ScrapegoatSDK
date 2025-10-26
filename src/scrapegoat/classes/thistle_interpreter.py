"""
"""

# IMPORTS
import re
from .thistle import Thistle
from .conditions import InCondition, IfCondition


class Token:
    """
    """
    def __init__(self, type: str, value: str, position: int = None, line: int = None):
        """
        """
        self.type = type
        self.value = value
        self.position = position
        self.line = line

    def __repr__(self):
        """
        """
        return f"Token(type={self.type}, value='{self.value}', position={self.position}, line={self.line})"
    

class ThistleInterpreter:
    """
    """
    ACTIONS = {"select", "scrape"}
    CONDITIONALS = {"if", "in"}
    KEYWORDS = {"position"}
    NEGATIONS = {"not"}
    FLAGS = {}
    OPERATORS = {"=", "!="}

    def __init__(self):
        """
        """
        pass

    def _tokenizer(self, query: str) -> list[Token]:
        """
        """
        tokens = []
        pattern = (r'(\bSELECT\b|\bSCRAPE\b|\bIN\b|\bIF\b|'r'!=|==|=|;|\n|'r'"(?:[^"]*)"|\'(?:[^\']*)\'|'r'@?[A-Za-z_][A-Za-z0-9_-]*|'r'\d+)')


        for match in re.finditer(pattern, query, flags=re.IGNORECASE):
            raw_value = match.group(0)
            position = match.start()
            line = query.count('\n', 0, position) + 1

            if raw_value[0] in ('"', "'") and raw_value[-1] == raw_value[0]:
                value = raw_value[1:-1]
                token_type = "IDENTIFIER"
            else:
                value = raw_value.lower()
                if value in self.ACTIONS:
                    token_type = "ACTION"
                elif value in self.CONDITIONALS:
                    token_type = "CONDITIONAL"
                elif value in self.KEYWORDS:
                    token_type = "KEYWORD"
                elif value in self.OPERATORS:
                    token_type = "OPERATOR"
                elif re.match(r'^\d+$', value):
                    token_type = "NUMBER"
                elif value in self.NEGATIONS:
                    token_type = "NEGATION"
                elif value in self.FLAGS:
                    token_type = "FLAG"
                elif re.match(r'^(?:"[^"]*"|\'[^\']*\'|@?[A-Za-z_][A-Za-z0-9_-]*)$', value):
                    token_type = "IDENTIFIER"
                    if value[0] in ("'", '"'):
                        value = value[1:-1]
                elif value == ";":
                    token_type = "SEMICOLON"
                else:
                    token_type = "UNKNOWN"

            tokens.append(Token(token_type, value, position, line))
        return tokens
        
    def _actions_parser(self, tokens, index) -> tuple:
        """
        """
        token = tokens[index]
        if token.type != "ACTION":
            raise SyntaxError(f"Expected SCRAPE or SELECT at token {token}")
        action = token.value
        index += 1
        return action, index

    def _count_parser(self, tokens, index) -> tuple:
        """
        """
        token = tokens[index]
        if token.type != "NUMBER":
            count = 0
        else:
            count = int(token.value)
            index += 1
        return count, index

    def _element_parser(self, tokens, index) -> tuple:
        """
        """
        token = tokens[index]
        if token.type != "IDENTIFIER":
            raise SyntaxError(f"Expected element at token {token}")
        element = token.value
        index += 1
        return element, index

    def _in_condition_parser(self, tokens, index, element, negated) -> tuple:
        """
        """
        token = tokens[index]
        if token.type == "KEYWORD":
            index += 1
            token = tokens[index]
            if token.type != "OPERATOR":
                raise SyntaxError(f"Expected '=' after IN POSITION at token {token}")
            if token.value == "!=":
                negated = True
            index += 1
            token = tokens[index]
            if token.type != "NUMBER":
                raise SyntaxError(f"Expected number after IN POSITION = at token {token}")
            position = int(token.value)
            condition = InCondition(target="POSITION", value=position, negated=negated, query_tag=element)
        else:
            if token.type != "IDENTIFIER":
                raise SyntaxError(f"Expected element after IN at token {token}")
            target = token.value
            condition = InCondition(target=target, negated=negated, query_tag=element)
        index += 1
        return condition, index
    
    def _if_condition_parser(self, tokens, index, element, negated) -> tuple:
        """
        """
        token = tokens[index]
        if token.type != "IDENTIFIER":
            raise SyntaxError(f"Expected key after IF at token {token}")
        key = token.value
        index += 1
        token = tokens[index]
        if token.type != "OPERATOR":
            raise SyntaxError(f"Expected '=' after IF {key} at token {token}")
        if token.value == "!=":
            negated = True
        index += 1
        token = tokens[index]
        if token.type not in {"IDENTIFIER", "NUMBER"}:
            raise SyntaxError(f"Expected value after IF {key} = at token {token}")
        value = token.value
        condition = IfCondition(key=key, value=value, negated=negated, query_tag=element)
        index += 1
        return condition, index

    def _conditions_parser(self, tokens, index, element) -> tuple:
        """
        """
        negated = False
        token = tokens[index]
        if token.type == "NEGATION":
            negated = True
            index += 1
            token = tokens[index]
        if token.type != "CONDITIONAL":
            raise SyntaxError(f"Expected conditional at token {token}")
        conditional = token.value
        index += 1

        if conditional == "in":
            condition, index = self._in_condition_parser(tokens, index, element, negated)
        elif conditional == "if":
            condition, index = self._if_condition_parser(tokens, index, element, negated)
        else:
            raise SyntaxError(f"Unknown conditional {conditional} at token {token}")
        
        return condition, index
    
    def interpret(self, query: str) -> list[Thistle]:
        """
        """
        tokens = self._tokenizer(query)
        instructions = []
            
        index = 0
        while index < len(tokens):
            action, index = self._actions_parser(tokens, index)
            count, index = self._count_parser(tokens, index)
            element, index = self._element_parser(tokens, index)

            # Conditions
            conditions = []
            token = tokens[index]
            while token.type != "SEMICOLON":
                condition, index = self._conditions_parser(tokens, index, element)
                conditions.append(condition)
                token = tokens[index]
                
            instructions.append(Thistle(action=action, count=count, element=element, conditions=conditions, flags=[]))
            index += 1

        return instructions
    
            
def main():
    """
    """
    pass


if __name__ == "__main__":
    main()
