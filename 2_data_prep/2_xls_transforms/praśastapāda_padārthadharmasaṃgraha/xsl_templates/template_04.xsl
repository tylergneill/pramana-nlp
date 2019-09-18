<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" encoding="UTF-8">
<xsl:output method="xml" indent="yes"/>
<xsl:strip-space elements="*" />

<xsl:template match="@*|node()">
<xsl:copy>
<xsl:apply-templates select="@*|node()"/>
</xsl:copy>
</xsl:template>

<xsl:template match="head">

{<xsl:value-of select="count(parent::div/preceding-sibling::div)+1"/>
<xsl:text> </xsl:text>
<xsl:value-of select="."/>}

</xsl:template>

<xsl:template match="div/p[@n2=0]">

[<xsl:value-of select="@n"/>]

<xsl:value-of select="."/>
</xsl:template>

<xsl:template match="div/p[not(@n2=0)]">
<xsl:value-of select="."/>
</xsl:template>


</xsl:stylesheet>
