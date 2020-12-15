<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" encoding="UTF-8">
<xsl:output method="xml" indent="yes"/>
<xsl:strip-space elements="*" />

<xsl:template match="@*|node()">
<xsl:copy>
<xsl:apply-templates select="@*|node()"/>
</xsl:copy>
</xsl:template>

<xsl:template match="//quote[not(@*) and child::lg]|//q[child::lg]">
<lg>
<quote>
<xsl:copy-of select="./lg/l"/>
</quote>
</lg>
</xsl:template>

<xsl:template match="ab">
<p>
<quote>
<xsl:value-of select="."/>
</quote>
</p>
</xsl:template>

</xsl:stylesheet>